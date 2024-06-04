from django.db import models
from fs_documents.models import Document
from fs_utils.constants import LOAN_STATUSES, STATUS_PENDING
from fs_utils.models import BaseModel
from fs_loan_types.models import LoanType


class Loan(BaseModel):

    loan_type = models.ForeignKey(
        LoanType, on_delete=models.CASCADE)
    borrower_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(null=True, blank=True)
    # Number of months for repayment
    loan_term = models.IntegerField(null=True, blank=True, default=3)
    due_date = models.DateTimeField(null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True,)
    disbursement_date = models.DateTimeField(null=True, blank=True,)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True)  # Annual interest rate
    amount = models.IntegerField()
    status = models.CharField(
        max_length=50, default=STATUS_PENDING, choices=LOAN_STATUSES)
    attachments = models.ManyToManyField(Document, related_name='items')

    def __str__(self):
        return f'{self.borrower_name} - {self.amount} - {self.loan_type}'
