from django.db.models.signals import post_save
from django.dispatch import receiver

from loans.models import Loan
from utils.constants import CREATED, UPDATED
from .models import LoanReport


@receiver(post_save, sender=Loan)
def create_loan_report(sender, instance, created, **kwargs):
    if created:
        action = CREATED
    else:
        action = UPDATED

    LoanReport.objects.create(
        loan_id=instance, action=action, status=instance.status,
        created_by=instance.created_by
    )
