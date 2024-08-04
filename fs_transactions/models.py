from django.db import models

from fs_audits.mixins import AuditTrailMixin
from fs_audits.models import AuditTrail
from fs_loans.models import Loan
from fs_utils.constants import CLOSED, REPAYMENT, TRANSACTION_CHOICES
from fs_utils.models import BaseModel
from fs_utils.utils import generate_unique_number

# Create your models here.


class Transaction(BaseModel):
    payment_number = models.CharField(
        max_length=20, unique=True, editable=False)
    loan = models.ForeignKey(
        Loan, related_name='transactions', on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TRANSACTION_CHOICES)

    def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = generate_unique_number("PAY")

        if self.type == REPAYMENT:
            # get balance after payment
            outstanding_balance = self.loan.outstanding_balance
            if outstanding_balance is not None:
                if outstanding_balance - self.amount <= 0:
                    self.loan.status = CLOSED
                    self.loan.save()
                    # Close loan

        # Create Audit for transaction on loan
        AuditTrail.objects.create(
            action="transaction",
            model_name="loan",
            object_id=self.loan.pk,
            actor=self.created_by,
            changes={'payment_number': self.payment_number,
                     'type': self.type, 'amount': self.amount},
        )

        super(Transaction, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.payment_number} - {self.loan.ref_number} - {self.amount}/='
