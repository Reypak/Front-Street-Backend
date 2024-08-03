from datetime import datetime
from rest_framework import viewsets

from fs_installments.models import Installment
from fs_transactions.filters import TransactionFilterSet
from fs_utils.constants import MISSED, NOT_PAID, PAID, PARTIALLY_PAID
from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = TransactionFilterSet
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # save transaction instance
        serializer.save()

        # repayment type
        if serializer.data['type'] == REPAYMENT:
            amount = serializer.data['amount']
            loan = serializer.data['loan']
            # filter installments by status
            installments = Installment.objects.filter(
                loan=loan,
                status__in=[MISSED, PARTIALLY_PAID]).order_by('id')

            # allocate payment to missed and partial paid
            for installment in installments:
                if amount <= 0:
                    break

                if installment.status in [MISSED, PARTIALLY_PAID]:
                    balance = installment.balance

                    if amount >= balance:  # if payment covers full balance
                        amount -= balance
                        installment.paid_amount = installment.total_amount
                        installment.status = PAID

                    else:  # for partially paid
                        # place remaining amount to installment
                        installment.paid_amount += amount
                        amount = 0
                        installment.status = PARTIALLY_PAID

                    installment.payment_date = datetime.today()
                    installment.save()

            # Handle remaining payment for current or future installments
            if amount > 0:
                future_installments = Installment.objects.filter(
                    loan=loan,
                    status=NOT_PAID).order_by('id')
                for installment in future_installments:
                    if amount <= 0:
                        break

                    if amount >= installment.total_amount:
                        amount -= installment.total_amount
                        installment.paid_amount = installment.total_amount
                        installment.status = PAID
                    else:
                        installment.paid_amount += amount
                        amount = 0
                        installment.status = PARTIALLY_PAID

                    installment.payment_date = datetime.today()
                    installment.save()

        return Response(status=200)


class TransactionList(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        loan_id = self.kwargs['loan_id']
        return Transaction.objects.filter(loan=loan_id)
