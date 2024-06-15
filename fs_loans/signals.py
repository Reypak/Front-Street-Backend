from django.db.models.signals import post_save
from django.dispatch import receiver

from fs_reports.models import LoanReport
from fs_loans.models import Loan
from fs_utils.constants import APPROVED, CREATED, DECLINED, DISBURSED, PENDING, UPDATED
from fs_utils.notifications.emails import send_templated_email


@receiver(post_save, sender=Loan)
def handle_loan(sender, instance, created, **kwargs):

    created_by = None
    loan_status = instance.status
    email = instance.email

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
            'user': instance.borrower_name,
            'application_number': instance.application_number,
            'status': get_loan_status(),
        }

        return send_templated_email(subject, 'loan_status.html', context, recipient_list)

    # List statuses to trigger email
    # if loan_status in [PENDING, APPROVED, DECLINED, DISBURSED]:
    #     if email is not None:
    #         return send_email()
