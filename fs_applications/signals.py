# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from fs_loans.models import Loan
from fs_utils.constants import ACCEPTED
from .models import Application


@receiver(post_save, sender=Application)
def create_loan_on_acceptance(sender, instance, created, **kwargs):
    if not created:  # Check if this is an update
        if instance.status == ACCEPTED and not Loan.objects.filter(application=instance).exists():
            loan = Loan.objects.create(
                application=instance,
                client=instance.client,
                category=instance.category,
                loan_term=instance.loan_term,
                interest_rate=instance.interest_rate,
                amount=instance.amount,
                payment_frequency=instance.payment_frequency,
                created_by=instance.updated_by
            )
            # call to create ref_number
            loan.generate_ref_number()
