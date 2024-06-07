from django.db.models.signals import post_save
from django.dispatch import receiver

from fs_reports.models import LoanReport
from fs_loans.models import Loan
from fs_utils.constants import CREATED, UPDATED


@receiver(post_save, sender=Loan)
def handle_loan(sender, instance, created, **kwargs):

    created_by = None

    if created:
        action = CREATED
        created_by = instance.created_by
    else:
        action = UPDATED
        if hasattr(instance, 'updated_by'):
            created_by = instance.updated_by

    # create_loan_report
    if created_by is not None:
        LoanReport.objects.create(
            loan=instance, action=action, status=instance.status,
            created_by=created_by
        )
