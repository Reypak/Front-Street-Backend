from rest_framework import viewsets
from fs_loans.filters import LoanFilterSet
from fs_utils.constants import DAILY, FIXED_MONTHLY, INTEREST_ONLY, MONTH_DAYS, MONTHLY
from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date, timedelta

from fs_utils.utils import calculate_loan_interest_rate


# from utils.constants import CustomPagination

# Create your views here.
# import local data
from .serializers import *
from .models import Loan
from rest_framework.permissions import IsAuthenticated

# create a viewset


class LoanViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Loan.objects.all()
    permission_classes = [IsAuthenticated]

    # specify serializer to be used
    # serializer_class = LoanSerializer

    # set data filters
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = LoanFilterSet

    def get_serializer_class(self):
        if self.action == 'list':
            return LoanListSerializer
        if self.action == 'retrieve':
            return LoanViewSerializer

        return LoanSerializer

    # for custom pagination
    # pagination_class = CustomPagination

    # def perform_create(self, serializer):
    #     return serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(updated_by=self.request.user)


class LoanScheduleView(APIView):
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
        payment_frequency = loan.payment_frequency
        loan_term = loan.loan_term
        interest_rate = loan.interest_rate
        disbursement_date = date.today() + timedelta(days=30)  # get current date
        repayment_type = request.data.get(
            'repayment_type') or loan.repayment_type

        interest_amount = interest_rate * principal / 100

        if payment_frequency == MONTHLY:
            if loan_term == 0:
                return Response({'error': 'Term months cannot be zero'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the loan interest
        loan_interest = calculate_loan_interest_rate(
            loan)

        installments = []

        # DAILY LOAN
        if payment_frequency == DAILY:
            current_date = datetime.now() + timedelta(days=1)
            for _ in range(MONTH_DAYS):
                # Find the next working day
                while current_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                    current_date += timedelta(days=1)
                installments.append({
                    'loan': loan.id,
                    'due_date': current_date.date(),
                    'amount': loan_interest['payment_amount'],
                    'interest': loan_interest['interest']
                })
                current_date += timedelta(days=1)

        # MONTHLY LOAN
        elif payment_frequency == MONTHLY:
            for i in range(loan_term):
                due_date = disbursement_date + timedelta(days=30 * (i + 1))
                # handle repayment type
                if repayment_type == INTEREST_ONLY:
                    if i == loan_term - 1:
                        # Final installment
                        installment = {
                            'loan': loan_id,
                            'due_date': due_date,
                            'interest': loan_interest['interest'],
                            'amount': principal,
                        }
                    else:
                        # Regular installments
                        installment = {
                            'loan': loan_id,
                            'due_date': due_date,
                            'interest': loan_interest['interest'],
                            'amount': 0,
                        }
                else:
                    # MONTHLY FIXED
                    installment = {
                        'loan': loan_id,
                        'due_date': due_date,
                        'interest': loan_interest['interest'],
                        'amount': loan_interest['payment_amount'],
                    }
                installments.append(installment)

        return Response({
            'loan_id': loan_id,
            'amount': principal,
            'interest_rate': interest_rate,
            'interest': interest_amount,
            'payment_amount': principal + interest_amount,
            'payment_frequency': payment_frequency,
            'loan_term': loan_term,
            'reypayment_type': repayment_type,
            'installments': installments
        })
