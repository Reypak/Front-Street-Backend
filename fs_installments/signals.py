# signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from fs_loans.models import Loan
# from fs_utils.constants import STATUS_DISBURSED
# from .models import Installment
# from datetime import timedelta


# @receiver(post_save, sender=Loan)
# def create_installments(sender, instance, created, **kwargs):
#     if not created and instance.status == STATUS_DISBURSED and not instance.installment_set.exists():
#         # Calculate monthly installment amount
#         monthly_interest_rate = instance.interest_rate / 12 / 100
#         num_payments = instance.term_months
#         principal = instance.amount

#         if monthly_interest_rate > 0:
#             monthly_payment = (principal * monthly_interest_rate) / \
#                 (1 - (1 + monthly_interest_rate) ** -num_payments)
#         else:
#             monthly_payment = principal / num_payments

#         # Generate installment records
#         for month in range(1, num_payments + 1):
#             due_date = instance.disbursement_date + timedelta(days=30*month)
#             Installment.objects.create(
#                 loan=instance,
#                 due_date=due_date,
#                 amount=monthly_payment
#             )

# Connect the signal
# post_save.connect(create_installments, sender=Loan)
