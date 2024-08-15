from datetime import datetime
from rest_framework import viewsets

from fs_charges.models import ChargePenalty
from fs_installments.models import Installment
from fs_transactions.filters import TransactionFilterSet
from fs_utils.constants import MISSED, NOT_PAID, OVERDUE, PAID, PARTIALLY_PAID
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilterSet
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # save transaction instance
        serializer.save()

        # repayment type
        if serializer.data['type'] == REPAYMENT:
            amount = serializer.data['amount']
            loan = serializer.data['loan']

            # print(loan.status)
            # if loan.status == ACTIVE:
            #     return

            # check for charges
            charge_penalties = ChargePenalty.objects.filter(
                loan=loan, status__in=[NOT_PAID, PARTIALLY_PAID]).order_by('id')
            # print('RUN CHARGE PENTALTIES')
            for charge in charge_penalties:
                if amount <= 0:
                    break
                # get balance
                balance = charge.balance
                # if payment covers full balance
                if amount >= balance:
                    amount -= balance
                    charge.paid_amount = charge.amount
                    charge.status = PAID
                else:
                    # for partially paid
                    charge.paid_amount += amount
                    amount = 0
                    charge.status = PARTIALLY_PAID
                # save the charge update
                charge.payment_date = datetime.today()
                charge.save(is_update=True)

            if amount > 0:
                # filter installments by status
                installments = Installment.objects.filter(
                    loan=loan,
                    status__in=[MISSED, OVERDUE, PARTIALLY_PAID]).order_by('id')
                # print('RUN INSTALLMENTS')
                # allocate payment to missed and partial paid
                for installment in installments:
                    if amount <= 0:
                        break

                    if installment.status in [MISSED, OVERDUE, PARTIALLY_PAID]:
                        balance = installment.balance

                        if amount >= balance:  # if payment covers full balance
                            amount -= balance
                            installment.paid_amount = installment.total_amount
                            installment.status = PAID

                        else:  # for partially paid
                            # place remaining amount to installment
                            installment.paid_amount += amount
                            amount = 0

                        installment.payment_date = datetime.today()
                        installment.save(update_loan=False)

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
                        installment.save(update_loan=False)

        return Response(status=200)


class TransactionList(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TransactionFilterSet

    def get_queryset(self):
        loan_id = self.kwargs['loan_id']
        return Transaction.objects.filter(loan=loan_id)
