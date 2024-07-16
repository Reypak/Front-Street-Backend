from rest_framework import viewsets
from datetime import datetime, date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from fs_installments.models import Installment
from fs_installments.serializers import InstallmentSerializer
from fs_loans.models import Loan
from fs_utils.constants import DAILY, DISBURSED, INTEREST_ONLY, MONTH_DAYS, MONTHLY
from fs_utils.utils import calculate_loan_interest_rate
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.


class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

# Get loan installments


class LoanInstallmentList(generics.ListAPIView):
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        loan_id = self.kwargs['loan_id']
        return Installment.objects.filter(loan=loan_id)


class LoanInstallmentCreateView(APIView):

    """
        Create multiple installments for a loan.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        installments = request.data
        if not isinstance(installments, list):
            return Response({"error": "Expected a list of objects"}, status=status.HTTP_400_BAD_REQUEST)

        # Pass installments to serializer
        serializer = InstallmentSerializer(data=installments, many=True)
        if serializer.is_valid():
            serializer.save()

            # Update loan status
            loan_id = installments[0]['loan']  # Extract the loan_id
            loan = Loan.objects.get(id=loan_id)
            loan.status = DISBURSED
            loan.save()

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

        interest_amount = interest_rate * principal / 100

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
                due_date = start_date + timedelta(days=30 * (i + 1))
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
            'installments': installments,
            'start_date': start_date
        })


def handle_date(request):
    # Get the 'start_date' parameter from the request
    start_date_str = request.GET.get('start_date', None)

    if start_date_str:
        # If the parameter is provided, parse it
        try:
            start_date = datetime.strptime(
                start_date_str, "%Y-%m-%d").date()
        except ValueError:
            # Handle the case where the date format is incorrect
            start_date = date.today()
    else:
        # If the parameter is not provided, use the current date
        start_date = date.today()

    return start_date
