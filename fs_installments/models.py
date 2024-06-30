from django.db import models

from fs_loans.models import Loan
from fs_utils.constants import INSTALLMENT_CHOICES, NOT_PAID

# Create your models here.


class Installment(models.Model):
    loan = models.ForeignKey(
        Loan, on_delete=models.DO_NOTHING, related_name='installments')
    fees_amount = models.IntegerField(default=0)
    interest = models.IntegerField(default=0)
    penalty_amount = models.IntegerField(default=0)
    due_date = models.DateField()
    amount = models.IntegerField()
    paid_amount = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=INSTALLMENT_CHOICES, default=NOT_PAID)
    payment_date = models.DateField(blank=True, null=True)

    # update loan due date
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.loan.save()

    @property
    def total_amount(self):
        return self.amount + self.interest + self.penalty_amount + self.fees_amount

    @property
    def balance(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f'Installment {self.id} for {self.loan.ref_number} - {self.status}, Balance: {self.balance}'
