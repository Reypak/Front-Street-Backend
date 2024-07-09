from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from fs_reports.models import LoanReport
from fs_loans.models import Loan
from fs_utils.constants import APPROVED, CANCELLED, CREATED, DECLINED, DISBURSED, PENDING, UPDATED
from fs_utils.notifications.emails import send_templated_email


@receiver(pre_save, sender=Loan)
def pre_save_loan(sender, instance, **kwargs):
    loan_status = instance.status

    if instance.pk:  # Check if the object exists
        old_status = Loan.objects.get(pk=instance.pk).status
        # set the old status from pre_save
        instance.old_status = old_status

        if old_status != loan_status:
            if loan_status == DISBURSED:
                instance.disbursement_date = timezone.now()
            elif loan_status == APPROVED:
                instance.approved_date = timezone.now()

    else:  # Create new object
        if loan_status == DISBURSED:
            instance.disbursement_date = timezone.now()
        elif loan_status == APPROVED:
            instance.approved_date = timezone.now()


@receiver(post_save, sender=Loan)
def handle_loan(sender, instance, created, **kwargs):

    created_by = None
    loan_status = instance.status

    # if hasattr(instance, 'email'):
    email = instance.client.email

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

    # Format status
    def get_loan_status():
        if loan_status == PENDING:
            return 'Created'
        return loan_status.capitalize()

    # Send emails
    def send_email():
        subject = f'Loan {get_loan_status()}'
        recipient_list = [email]

        context = {
            'user': instance.client.first_name,
            'application_number': instance.ref_number,
            'status': get_loan_status(),
        }

        return send_templated_email(subject, 'loan_status.html', context, recipient_list)

    # List statuses to trigger email
    if loan_status in [PENDING, APPROVED, CANCELLED, DISBURSED]:
        # get old status from instance
        if (hasattr(instance, 'old_status')):
            old_status = instance.old_status

        if instance.pk:
            old_status = Loan.objects.get(pk=instance.pk).status

        if old_status != loan_status and email is not None:
            return send_email()
