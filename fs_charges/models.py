from django.db import models
from fs_loans.models import Loan
from fs_utils.constants import CHARGE_CHOICES
from fs_utils.models import BaseModel


class Charge(BaseModel):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=CHARGE_CHOICES)
    description = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.amount})'


class ChargePenalty(BaseModel):
    loan = models.ForeignKey(
        Loan, on_delete=models.DO_NOTHING, related_name='charge_penalties')
    type = models.CharField(max_length=10, choices=CHARGE_CHOICES)
    amount = models.PositiveIntegerField()
    comment = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.type} ({self.amount}) on {self.loan.ref_number}'
