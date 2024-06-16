from rest_framework import viewsets
from datetime import datetime, date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from fs_installments.models import Installment
from fs_installments.serializers import InstallmentSerializer
from fs_loans.models import Loan
from fs_utils.constants import DAILY, DISBURSED, MONTHLY
from fs_utils.utils import calculate_interest_rate, calculate_loan_interest_rate
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.


class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]


class CalculateInstallmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        loan_id = request.data.get('loan_id')

        if loan_id is None:
            return Response({'error': 'Missing loan_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

        principal = loan.amount
        loan_type = loan.loan_type
        loan_term = loan.loan_term
        interest_rate = loan.interest_rate
        disbursement_date = date.today() + timedelta(days=30)  # get current date

        if loan_type == MONTHLY:
            if loan_term == 0:
                return Response({'error': 'Term months cannot be zero'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the monthly installment amount
        installment_amount = calculate_loan_interest_rate(
            loan)

        installments = []

        # DAILY LOAN
        if loan.loan_type == DAILY:
            current_date = datetime.now() + timedelta(days=1)
            for _ in range(30):
                # Find the next working day
                while current_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                    current_date += timedelta(days=1)
                installments.append({
                    'loan': loan.id,
                    'due_date': current_date.date(),
                    'amount': installment_amount
                })
                current_date += timedelta(days=1)

        # MONTHLY LOAN
        elif loan.loan_type == MONTHLY:
            for i in range(loan_term):
                due_date = disbursement_date + timedelta(days=30 * (i + 1))
                installments.append({
                    'loan': loan_id,
                    'due_date': due_date,
                    'amount': installment_amount
                })

        return Response({
            'loan_id': loan_id,
            'loan_type': loan_type,
            'amount': principal,
            'interest_rate': interest_rate,
            'loan_term': loan_term,
            'installments': installments
        })


class LoanInstallmentCreateView(APIView):
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

# Get loan installments


class LoanInstallmentList(generics.ListAPIView):
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        loan_id = self.kwargs['loan_id']
        return Installment.objects.filter(loan=loan_id)
