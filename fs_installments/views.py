from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from fs_loans.models import Loan
from fs_utils.utils import calculate_interest_rate

# Create your views here.


class CalculateInstallmentsView(APIView):
    def get(self, request, *args, **kwargs):
        loan_id = request.data.get('loan_id')

        if loan_id is None:
            return Response({'error': 'Missing loan_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

        principal = loan.amount
        loan_term = loan.loan_term
        interest_rate = loan.interest_rate
        disbursement_date = date.today()  # get current date

        if loan_term == 0:
            return Response({'error': 'Term months cannot be zero'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the monthly installment amount
        monthly_installment = calculate_interest_rate(
            principal, interest_rate, loan_term)
        installments = []

        for i in range(loan_term):
            due_date = disbursement_date + timedelta(days=30 * (i + 1))
            installments.append({
                'due_date': due_date,
                'amount': monthly_installment
            })

        return Response({
            'loan_id': loan_id,
            'amount': principal,
            'interest_rate': interest_rate,
            'loan_term': loan_term,
            'installments': installments
        })
