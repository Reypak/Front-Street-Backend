from datetime import datetime
from rest_framework import viewsets

from fs_installments.models import Installment
from fs_utils.constants import MISSED, NOT_PAID, PAID, PARTIALLY_PAID
from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from fs_utils.filters.filters import LoanPaymentFilterSet
from .serializers import LoanPaymentSerializer
from .models import LoanPayment
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.


class LoanPaymentViewSet(viewsets.ModelViewSet):
    queryset = LoanPayment.objects.all()
    serializer_class = LoanPaymentSerializer
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = LoanPaymentFilterSet
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # save payment instance
        serializer.save()

        amount_paid = serializer.data['amount_paid']
        # filter installments by status
        installments = Installment.objects.filter(
            status__in=[MISSED, PARTIALLY_PAID]).order_by('id')

        # allocate payment to missed and partial paid
        for installment in installments:
            if amount_paid <= 0:
                break

            if installment.status in [MISSED, PARTIALLY_PAID]:
                balance = installment.balance

                if amount_paid >= balance:  # if payment covers full balance
                    amount_paid -= balance
                    installment.paid_amount = installment.amount
                    installment.status = PAID

                else:  # for partially paid
                    # place remaining amount to installment
                    installment.paid_amount += amount_paid
                    amount_paid = 0
                    installment.status = PARTIALLY_PAID

                installment.payment_date = datetime.today()
                installment.save()

        # Handle remaining payment for current or future installments
        if amount_paid > 0:
            future_installments = Installment.objects.filter(
                status=NOT_PAID).order_by('id')
            for installment in future_installments:
                if amount_paid <= 0:
                    break

                if amount_paid >= installment.amount:
                    amount_paid -= installment.amount
                    installment.paid_amount = installment.amount
                    installment.status = PAID
                else:
                    installment.paid_amount += amount_paid
                    amount_paid = 0
                    installment.status = PARTIALLY_PAID

                installment.payment_date = datetime.today()
                installment.save()

        return Response(installments)


class LoanPaymentsList(generics.ListAPIView):
    serializer_class = LoanPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        loan_id = self.kwargs['loan_id']
        return LoanPayment.objects.filter(loan=loan_id)
