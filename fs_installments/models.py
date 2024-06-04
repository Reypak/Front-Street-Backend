from django.db import models

from fs_loans.models import Loan
from fs_utils.constants import CURRENT, INSTALLMENT_CHOICES

# Create your models here.


class Installment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    due_date = models.DateField()
    amount = models.IntegerField()
    paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10, choices=INSTALLMENT_CHOICES, default=CURRENT)
    payment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Installment {self.id} for Loan {self.loan.id}'
