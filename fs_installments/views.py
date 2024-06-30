from rest_framework import viewsets
from datetime import datetime, date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from fs_installments.models import Installment
from fs_installments.serializers import InstallmentSerializer
from fs_loans.models import Loan
from fs_utils.constants import DAILY, DISBURSED, MONTHLY
from fs_utils.utils import calculate_loan_interest_rate
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.


class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]


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

# Get loan installments


class LoanInstallmentList(generics.ListAPIView):
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        loan_id = self.kwargs['loan_id']
        return Installment.objects.filter(loan=loan_id)
