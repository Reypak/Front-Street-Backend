from django.db import models

from fs_audits.mixins import AuditTrailMixin
from fs_loans.models import Loan
from fs_utils.constants import INSTALLMENT_CHOICES, NOT_PAID
from fs_utils.models import BaseModel

# Create your models here.


class Installment(AuditTrailMixin, BaseModel):
    loan = models.ForeignKey(
        Loan, on_delete=models.DO_NOTHING, related_name='installments')
    fees = models.IntegerField(default=0)
    interest = models.IntegerField(default=0)
    penalty = models.IntegerField(default=0)
    due_date = models.DateField()
    principal = models.PositiveIntegerField()
    paid_amount = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=INSTALLMENT_CHOICES, default=NOT_PAID)
    payment_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    # update loan due date
    def save(self, *args, update_loan=True, **kwargs):
        super().save(*args, **kwargs)
        if update_loan:
            self.loan.update_due_date()

    @property
    def total_amount(self):
        return self.principal + self.interest + self.penalty + self.fees

    @property
    def balance(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f'Installment {self.id} for {self.loan.ref_number} - {self.status}, Balance: {self.balance}'
