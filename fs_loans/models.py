from django.db import models
from django.db.models import Sum, F
from fs_applications.models import Application, LoanApplicationBaseModel
from fs_documents.models import Document
from fs_utils.constants import ACTIVE, CANCELLED, FIXED_INTEREST, LOAN_STATUSES, MISSED, OVERDUE, PENDING, REPAYMENT, REPAYMENT_TYPES


class Loan(LoanApplicationBaseModel):
    # comments = GenericRelation(Comment)

    repayment_type = models.CharField(
        max_length=50, default=FIXED_INTEREST, choices=REPAYMENT_TYPES)

    # loan application instance
    application = models.OneToOneField(
        Application, related_name="loan", on_delete=models.DO_NOTHING, null=True, blank=True)

    end_date = models.DateField(null=True, blank=True)
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

    # update loan due date
    def save(self, *args, **kwargs):
        if self.pk is not None:
            last_installment = self.installments.order_by('-due_date').first()
            if last_installment:
                self.end_date = last_installment.due_date
        super().save(*args, **kwargs)

    @property
    def payment_amount(self):
        total_installments = self.installments.aggregate(
            total=Sum(F('principal') + F('penalty') + F('fees') + F('interest')))['total'] or 0
        return total_installments

    @property
    def amount_paid(self):
        # Iterate through the payments
        total_payments = self.transactions.filter(type=REPAYMENT).aggregate(
            total=models.Sum('amount'))['total'] or 0
        return total_payments

    @property
    def outstanding_balance(self):
        # set outstanding_balance
        if self.status in [ACTIVE, CANCELLED]:
            return self.payment_amount - self.amount_paid

    # overdue_amount
    @property
    def overdue(self):
        if self.status in [ACTIVE]:
            total_amount = F('principal') + F('penalty') + \
                F('fees') + F('interest')
            paid_amount = F('paid_amount')
            overdue_amount = self.installments.filter(status=OVERDUE).aggregate(
                # calculate the installment balance
                total=Sum(total_amount - paid_amount))['total'] or 0
            return overdue_amount

    def __str__(self):
        return f'{self.ref_number}: {self.amount}/= : {self.client.first_name}'
