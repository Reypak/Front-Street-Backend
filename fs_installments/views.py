from rest_framework import viewsets
from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from fs_installments.models import Installment
from fs_installments.serializers import InstallmentSerializer
from fs_loans.models import Loan
from fs_utils.constants import DISBURSED
from fs_utils.utils import calculate_interest_rate
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
                'loan': loan_id,
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
