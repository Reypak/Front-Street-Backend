from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.utils import timezone
from datetime import datetime, date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fs_audits.models import AuditTrail
from fs_installments.filters import InstallmentFilterSet
from fs_installments.models import Installment
from fs_installments.serializers import InstallmentSerializer, RescheduleSerializer
from fs_loans.models import Loan
from fs_utils.constants import ACTIVE, DAILY, DATE_FORMAT, INTEREST_ONLY, LOAN, MISSED, MONTH_DAYS, MONTHLY, NOT_PAID, OVERDUE, PARTIALLY_PAID, REMINDER, SCHEDULE, SECRET_TOKEN
from fs_utils.notifications.emails import send_templated_email
from fs_utils.utils import calculate_loan_interest_rate, format_number
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.


class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = InstallmentFilterSet

    def perform_update(self, serializer):
        # pass request user
        installment = serializer.save(updated_by=self.request.user)
        return installment


# Get loan installments
# class LoanInstallmentList(generics.ListAPIView):
#     serializer_class = InstallmentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         loan_id = self.kwargs['loan_id']
#         return Installment.objects.filter(loan=loan_id)


class PaymentScheduleCreateView(APIView):
    """
        Create multiple installments for a loan.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        installments = request.data.get('installments')
        if not isinstance(installments, list):
            return Response({"installments": "Expected a list of objects"}, status=status.HTTP_400_BAD_REQUEST)

        # Pass installments to serializer
        serializer = InstallmentSerializer(
            data=installments, many=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            # Update loan status
            # loan_id = installments[0]['loan']  # Extract the loan_id
            # loan = Loan.objects.get(id=loan_id)
            # loan.status = DISBURSED
            # loan.save()

            # AUDIT TRAIL
            AuditTrail.objects.create(
                action=SCHEDULE,
                model_name=LOAN,
                object_id=installments[0]['loan'],
                actor=request.user,
                changes={'schedule': 'created'}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentScheduleView(APIView):
    """
        Create preview list of all installments for a loan.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # loan_id = request.data.get('loan_id')
        loan_id = self.kwargs['loan_id']

        if loan_id is None:
            return Response({'error': 'Missing loan_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

        principal = loan.amount
        interest_rate = loan.interest_rate

        start_date = handle_date(request)  # get start date
#
        repayment_type = request.GET.get('repayment_type', loan.repayment_type)

        loan_term = int(request.GET.get('loan_term', loan.loan_term))

        payment_frequency = request.GET.get(
            'payment_frequency', loan.payment_frequency)

        interest_amount = interest_rate / 100 * principal

        if payment_frequency == MONTHLY:
            if loan_term == 0:
                return Response({'error': 'Term months cannot be zero'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the loan interest
        loan_interest = calculate_loan_interest_rate(
            principal, interest_rate, payment_frequency, loan_term)

        installments = []

        # DAILY LOAN
        if payment_frequency == DAILY:
            current_date = start_date + timedelta(days=1)
            for _ in range(MONTH_DAYS):
                # Find the next working day
                while current_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                    current_date += timedelta(days=1)
                installments.append({
                    'loan': loan.id,
                    'due_date': current_date,
                    'principal': loan_interest['principal'],
                    'interest': loan_interest['interest'],
                    'total': loan_interest['total']
                })
                current_date += timedelta(days=1)

        # MONTHLY LOAN
        elif payment_frequency == MONTHLY:
            for i in range(loan_term):
                due_date = start_date + timedelta(days=MONTH_DAYS * (i + 1))
                # handle repayment type
                if repayment_type == INTEREST_ONLY:
                    if i == loan_term - 1:
                        # Final installment
                        installment = {
                            'loan': loan_id,
                            'due_date': due_date,
                            'interest': loan_interest['interest'],
                            'principal': principal,
                            'total': loan_interest['interest'] + principal
                        }
                    else:
                        # Regular installments
                        installment = {
                            'loan': loan_id,
                            'due_date': due_date,
                            'interest': loan_interest['interest'],
                            'principal': 0,
                            'total': loan_interest['interest']

                        }
                else:
                    # MONTHLY FIXED
                    installment = {
                        'loan': loan_id,
                        'due_date': due_date,
                        'interest': loan_interest['interest'],
                        'principal': loan_interest['principal'],
                        'total': loan_interest['total']

                    }
                installments.append(installment)

        return Response({
            'loan_id': loan_id,
            'principal': principal,
            'interest_rate': interest_rate,
            'interest': interest_amount,
            'total': principal + interest_amount,
            'payment_frequency': payment_frequency,
            'loan_term': loan_term,
            'repayment_type': repayment_type,
            'start_date': start_date,
            'installments': installments,
        })


class RescheduleInstallmentView(APIView):
    def post(self, request):
        # Validate the request data
        serializer = RescheduleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        loan_id = serializer.validated_data['loan']
        loan_term = serializer.validated_data['loan_term']
        start_date = serializer.validated_data['start_date']
        # interest_rate = serializer.validated_data['interest_rate']
        amount = serializer.validated_data['amount']

        # Fetch the loan object
        loan = get_object_or_404(Loan, id=loan_id)

        # Rescheduling logic
        # loan.update_remaining_balance()
        # remaining_balance = loan.remaining_balance

        # Remove existing unpaid installments
        loan.installments.filter(status=NOT_PAID).delete()

        # Calculate the new installment amount
        new_installment_amount = amount / loan_term
        # current_date = timezone.now().date()

        # Create new installments
        new_installments = []
        for i in range(loan_term):
            # Assume each month is roughly 30 days
            due_date = start_date + timedelta(days=(i * MONTH_DAYS))
            new_installment = {
                'loan': loan.id,
                'due_date': due_date,
                'principal': new_installment_amount,
            }
            new_installments.append(new_installment)

        serializer = InstallmentSerializer(
            data=new_installments, many=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()

        # Assign the new installments to the loan
        # loan.installments.add(*new_installments)
        # loan.duration_in_months = new_duration_in_months
        # loan.num_of_installments = new_duration_in_months
        # loan.save()

        return Response({"message": "Loan installments have been rescheduled successfully."}, status=status.HTTP_200_OK)


def handle_date(request):
    # Get the 'start_date' parameter from the request
    start_date_str = request.GET.get('start_date', None)

    if start_date_str:
        # If the parameter is provided, parse it
        try:
            start_date = datetime.strptime(
                start_date_str, DATE_FORMAT).date()
        except ValueError:
            # Handle the case where the date format is incorrect
            start_date = date.today()
    else:
        # If the parameter is not provided, use the current date
        start_date = date.today()

    return start_date


def check_installments(request):
    """
        Check installment dates and update status accordingly
    """
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header == f'Bearer {SECRET_TOKEN}':
            today = timezone.now().date().today()

            # OVERDUE
            overdue_installments = Installment.objects.filter(
                due_date=today,
                status__in=[NOT_PAID, PARTIALLY_PAID],
                loan__status=ACTIVE)

            loans = Loan.objects.filter(
                id__in=overdue_installments.values_list('loan_id', flat=True)
            )
            # Update the related loans
            loans.update(is_overdue=True)
            # Update installment status to OVERDUE
            overdue_installments.update(status=OVERDUE)

            # MISSED
            missed_installments = Installment.objects.filter(
                due_date__lt=today,
                status__in=[NOT_PAID, OVERDUE],
                loan__status=ACTIVE)
            missed_installments.update(status=MISSED)

            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def send_reminders(request):
    """
        Check installment dates and send reminder notifications
    """
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header == f'Bearer {SECRET_TOKEN}':
            today = date.today()

            # REMAINDER
            reminder_period = today + timedelta(days=3)
            not_paid_installments = Installment.objects.filter(
                due_date=reminder_period,
                status=NOT_PAID,
                loan__status=ACTIVE,
                loan__payment_frequency=MONTHLY,
            )

            # DUE PAYEMENTS
            due_installments = Installment.objects.filter(
                due_date=today,
                status__in=[NOT_PAID, OVERDUE],
                loan__status=ACTIVE,
                loan__payment_frequency=MONTHLY,
            )

            # email_list = []  # mailing list
            # emails = []  # addresses

            # REMINDERS
            for installment in not_paid_installments:
                loan = installment.loan
                client = loan.client
                email = client.email
                total_amount = installment.total_amount
                due_date = installment.due_date

                subject = 'Upcoming Payment Reminder'
                recipient_list = [email]

                context = {
                    'name': client.first_name,
                    'ref_number': loan.ref_number,
                    'total': f'{format_number(total_amount)}/=',
                    'due_date': due_date,
                    'description': f'Installment payment for {loan.ref_number}',
                }

                send_templated_email(
                    subject, 'payment_reminder.html', context, recipient_list)

                # email_tuple = prepare_templated_email(
                #     subject, 'payment_reminder.html', context, recipient_list)
                # Accumulate Emails in a List
                # email_list.append(email_tuple)
                # emails.append(context)

                # AUDIT TRAIL

                AuditTrail.objects.create(
                    action=REMINDER,
                    model_name=LOAN,
                    object_id=loan.pk,
                    changes={'email': f'sent to {email}',
                             'reminder_period': '3 days', 'due_date': due_date.strftime(DATE_FORMAT)},
                )

            # DUE PAYEMENTS
            for installment in due_installments:
                loan = installment.loan
                client = loan.client
                email = client.email
                total_amount = installment.total_amount
                due_date = installment.due_date

                subject = 'Due Payment Reminder'
                recipient_list = [email]

                context = {
                    'name': client.first_name,
                    'ref_number': loan.ref_number,
                    'total': f'{format_number(total_amount)}/=',
                    'due_date': due_date,
                    'period': ' (Today)',
                    'description': f'Installment payment for {loan.ref_number}',
                }

                send_templated_email(
                    subject, 'payment_reminder.html', context, recipient_list)

                # email_tuple = prepare_templated_email(
                #     subject, 'payment_reminder.html', context, recipient_list)
                # Accumulate Emails in a List
                # email_list.append(email_tuple)
                # emails.append(context)

                # AUDIT TRAIL

                AuditTrail.objects.create(
                    action=REMINDER,
                    model_name=LOAN,
                    object_id=loan.pk,
                    changes={'email': f'sent to {email}',
                             'status': 'Payment due', 'due_date': due_date.strftime(DATE_FORMAT)},
                )

            # print('SENDING MASS MAIL', emails)

            # return JsonResponse({'status': emails}, status=200)

            # Send all the emails at once
            # send_mass_mail(email_list)

            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
