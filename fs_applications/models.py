from django.db import models

from fs_categories.models import Category
from fs_clients.models import Client
from fs_documents.models import Document
from fs_utils.constants import APPLICATION_STATUS_CHOICES, PAYMENT_FREQUENCY_CHOICES, PENDING
from fs_utils.models import BaseModel

# Create your models here.


class LoanApplicationBaseModel(BaseModel):
    # application number
    ref_number = models.CharField(
        max_length=100, null=True, blank=True, editable=False)

    # client/borrower
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)

    # loan category
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING)
    payment_frequency = models.CharField(
        max_length=50, choices=PAYMENT_FREQUENCY_CHOICES)
    # number of months
    loan_term = models.PositiveIntegerField(null=True, blank=True, default=0)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    amount = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Application(LoanApplicationBaseModel):

    status = models.CharField(
        max_length=50, default=PENDING, choices=APPLICATION_STATUS_CHOICES)

    attachments = models.ManyToManyField(
        Document, related_name='application_attachments')

    def __str__(self):
        return f'{self.ref_number}: {self.client.first_name}'
