# signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from fs_loans.models import Loan
from fs_utils.constants import ACCEPTED, CANCELLED, PENDING, REJECTED
from fs_utils.notifications.emails import send_templated_email
from .models import Application


@receiver(pre_save, sender=Application)
def on_pre_save(sender, instance, **kwargs):

    if instance.pk:  # Check if the object exists
        old_status = Application.objects.get(pk=instance.pk).status

        # set the old status from pre_save
        instance.old_status = old_status


@receiver(post_save, sender=Application)
def create_loan_on_acceptance(sender, instance, created, **kwargs):
    email = instance.client.email
    status = instance.status

    if created:
        instance.ref_number = f"FS/LOA/{instance.id}"
    else:  # Check if this is an update
        if status == ACCEPTED and not Loan.objects.filter(application=instance).exists():
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

    # Format status
    def get_status(status):
        if status == PENDING:
            return f'Received'
        return status.capitalize()

     # List statuses to trigger email
    if status in [PENDING, CANCELLED, REJECTED]:
        # get old status from instance
        if (hasattr(instance, 'old_status')):
            old_status = instance.old_status

            if old_status != status and email is not None:
                return send_email("application", email, instance, get_status(status))

        else:
            if status and email is not None:
                return send_email("application", email, instance, get_status(status))

 # Send emails


def send_email(type, email, instance, status):
    subject = f'{type.capitalize()} {status.capitalize()}'
    recipient_list = [email]

    context = {
        'name': instance.client.first_name,
        'ref_number': instance.ref_number,
        'status': status,
        'type': type
    }

    return send_templated_email(subject, 'status_update.html', context, recipient_list)
