from datetime import datetime
import uuid
from django.db import models

from fs_loans.models import Loan
from fs_utils.models import BaseModel
from fs_utils.utils import generate_unique_number

# Create your models here.


class LoanPayment(BaseModel):
    payment_number = models.CharField(
        max_length=20, unique=True, editable=False)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = generate_unique_number("PAY")
        super(LoanPayment, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.payment_number} - {self.amount}/='
