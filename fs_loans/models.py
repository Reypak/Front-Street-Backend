from django.db import models
from fs_applications.models import Application, LoanApplicationBaseModel
from fs_documents.models import Document
from fs_utils.constants import LOAN_STATUSES, PENDING


class Loan(LoanApplicationBaseModel):

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

    def __str__(self):
        return f'{self.ref_number}: {self.amount}/= : {self.client.first_name}'
