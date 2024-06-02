from django.db import models
from documents.models import Document
from utils.constants import LOAN_STATUSES, STATUS_PENDING
from utils.models import BaseModel
from categories.models import Category


class Loan(BaseModel):

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    borrower_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    due_date = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    amount = models.IntegerField()
    status = models.CharField(
        max_length=50, default=STATUS_PENDING, choices=LOAN_STATUSES)
    attachments = models.ManyToManyField(Document, related_name='items')

    def __str__(self):
        return self.borrower_name + ' - ' + str(self.amount) + ' - ' + str(self.category)
