from django.db import models
from fs_categories.models import Category
from fs_documents.models import Document
from fs_utils.constants import LOAN_STATUSES, LOAN_TYPES, PENDING
from fs_utils.models import BaseModel


class Loan(BaseModel):
    application_number = models.CharField(
        max_length=100, null=True, blank=True)
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPES)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING)
    borrower_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(null=True, blank=True)
    # Number of months for repayment
    loan_term = models.PositiveIntegerField(null=True, blank=True, default=0)
    due_date = models.DateTimeField(null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True,)
    disbursement_date = models.DateTimeField(null=True, blank=True,)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True)  # Annual interest rate
    amount = models.IntegerField()
    status = models.CharField(
        max_length=50, default=PENDING, choices=LOAN_STATUSES)
    attachments = models.ManyToManyField(Document, related_name='documents')

    # def save(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     print('created_by', user)
    #     if user:
    #         if not self.pk:
    #             self.created_by = user
    #         self.created_by = user
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.application_number}: {self.amount}/='
