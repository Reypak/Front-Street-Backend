from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from fs_applications.signals import send_email
from fs_loans.models import Loan
from fs_utils.constants import APPROVED, CANCELLED, ACTIVE, PENDING


@receiver(pre_save, sender=Loan)
def pre_save_loan(sender, instance, **kwargs):
    loan_status = instance.status

    if instance.pk:  # Check if the object exists
        old_status = Loan.objects.get(pk=instance.pk).status
        # set the old status from pre_save
        instance.old_status = old_status

        if old_status != loan_status:
            if loan_status == ACTIVE:
                instance.disbursement_date = timezone.now()
            elif loan_status == APPROVED:
                instance.approved_date = timezone.now()

    else:  # Create new object
        if loan_status == ACTIVE:
            instance.disbursement_date = timezone.now()
        elif loan_status == ACTIVE:
            instance.approved_date = timezone.now()


@receiver(post_save, sender=Loan)
def handle_loan(sender, instance, created, **kwargs):

    # created_by = None
    loan_status = instance.status

    # if hasattr(instance, 'email'):
    email = instance.client.email

    if created:
        # action = CREATED
        # created_by = instance.created_by
        # set loan ref number
        instance.ref_number = f"FS/LOA/{instance.id}"
    # else:
        # action = UPDATED
        # if hasattr(instance, 'updated_by'):
        # created_by = instance.updated_by

    # create_loan_report
    # if created_by is not None:
    #     LoanReport.objects.create(
    #         loan=instance, action=action, status=instance.status,
    #         created_by=created_by
    #     )

    # Format status
    def get_status():
        if loan_status == PENDING:
            return 'created'
        elif loan_status == ACTIVE:
            return 'disbursed'
        return loan_status

    # List statuses to trigger email
    if loan_status in [PENDING, APPROVED, CANCELLED, ACTIVE]:
        # get old status from instance
        if (hasattr(instance, 'old_status')):
            old_status = instance.old_status

            if old_status != loan_status and email is not None:
                return send_email("loan", email, instance, get_status())

        else:
            if loan_status and email is not None:
                return send_email("loan", email, instance, get_status())

        # if instance.pk:
        #     old_status = Loan.objects.get(pk=instance.pk).status

        # if old_status != loan_status and email is not None:
        #     return send_email()
