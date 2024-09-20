from django.db import models
from fs_audits.mixins import AuditTrailMixin
from fs_categories.models import Category
from fs_documents.models import Document
from fs_users.models import CustomUser
from fs_utils.constants import APPLICATION_STATUS_CHOICES, CAN_CHANGE_APPLICATION_STATUS, MONTHLY, PAYMENT_FREQUENCY_CHOICES, PENDING
from fs_utils.models import BaseModel

# Create your models here.


class LoanApplicationBaseModel(BaseModel):
    # application number
    ref_number = models.CharField(
        max_length=100, null=True, blank=True, editable=False)

    # loan category
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING)

    payment_frequency = models.CharField(
        max_length=50, choices=PAYMENT_FREQUENCY_CHOICES, default=MONTHLY)
    # number of months
    loan_term = models.PositiveIntegerField(null=True, blank=True, default=0)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    amount = models.PositiveIntegerField()

    # client / borrower
    client = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING,
        # use the class name in the related name
        related_name="%(class)s_client"
    )

    class Meta:
        abstract = True


class Application(AuditTrailMixin, LoanApplicationBaseModel):

    status = models.CharField(
        max_length=50, default=PENDING, choices=APPLICATION_STATUS_CHOICES)

    attachments = models.ManyToManyField(
        Document, related_name='application_attachments')

    class Meta:
        ordering = ['-created_at']
        permissions = (
            (CAN_CHANGE_APPLICATION_STATUS, "Can change application status"),
        )

    def __str__(self):
        return f'{self.ref_number}'
