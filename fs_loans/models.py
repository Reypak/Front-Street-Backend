from django.db import models
from fs_applications.models import Application, LoanApplicationBaseModel
from fs_documents.models import Document
from fs_users.models import CustomUser
from fs_utils.constants import FIXED_MONTHLY, LOAN_STATUSES, PENDING, REPAYMENT_TYPES


class Loan(LoanApplicationBaseModel):

    repayment_type = models.CharField(
        max_length=50, default=FIXED_MONTHLY, choices=REPAYMENT_TYPES)

    # loan application instance
    application = models.OneToOneField(
        Application, on_delete=models.DO_NOTHING, null=True, blank=True)

    due_date = models.DateTimeField(null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True,)
    disbursement_date = models.DateTimeField(null=True, blank=True,)

    status = models.CharField(
        max_length=50, default=PENDING, choices=LOAN_STATUSES)

    attachments = models.ManyToManyField(
        Document, related_name='loan_attachments', blank=True)

    # def save(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     print('created_by', user)
    #     if user:
    #         if not self.pk:
    #             self.created_by = user
    #         self.created_by = user
    #     super().save(*args, **kwargs)

    def generate_ref_number(self):
        self.ref_number = f"FS/LOA/{self.id}"
        self.save()

    @property
    def outstanding_balance(self):
        # Iterate through the payments
        total_payments = self.payments.aggregate(
            total=models.Sum('amount_paid'))['total'] or 0
        # set outstanding_balance
        return self.amount - total_payments

    def __str__(self):
        return f'{self.ref_number}: {self.amount}/= : {self.client.first_name}'
