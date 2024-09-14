from django.db import models
from django.db.models import Sum, F
from fs_applications.models import Application, LoanApplicationBaseModel
from fs_audits.mixins import AuditTrailMixin
from fs_documents.models import Document
from django.utils.timezone import now
from fs_utils.constants import ACTIVE, CANCELLED, FIXED_INTEREST, LOAN_STATUSES, MISSED, NOT_PAID, OVERDUE, PARTIALLY_PAID, PENDING, REPAYMENT, REPAYMENT_TYPES


class Loan(AuditTrailMixin, LoanApplicationBaseModel):
    # comments = GenericRelation(Comment)

    repayment_type = models.CharField(
        max_length=50, default=FIXED_INTEREST, choices=REPAYMENT_TYPES)

    # loan application instance
    application = models.OneToOneField(
        Application, related_name="loan", on_delete=models.DO_NOTHING, null=True, blank=True)

    end_date = models.DateField(null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True,)

    status = models.CharField(
        max_length=50, default=PENDING, choices=LOAN_STATUSES)

    attachments = models.ManyToManyField(
        Document, related_name='loan_attachments', blank=True)

    # Flags
    is_overdue = models.BooleanField(default=False)

    def generate_ref_number(self):
        self.ref_number = f"FS/LOA/{self.id}"
        self.save()

    # update loan due date
    def update_due_date(self):
        if self.pk is not None:
            last_installment = self.installments.order_by('-due_date').first()
            if last_installment:
                self.end_date = last_installment.due_date
                self.updated_by = None  # core update
                self.save()

    # update flag status
    def update_flags(self):
        if self.is_overdue == True:
            if self.overdue <= 0:
                self.is_overdue = False
                self.save()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    @property
    def payment_amount(self):
        # get all installments
        total_installments = self.installments.aggregate(
            total=Sum(F('principal') + F('interest')))['total'] or 0
        return total_installments + self.charges

    @property
    def charges(self):
        # get all charges
        total_charges = self.charge_penalties.aggregate(total=Sum('amount'))[
            'total'] or 0
        return total_charges

    # @property
    # def charges(self):
    #     # get all charges
    #     charges_balance = self.charge_penalties.aggregate(total=Sum(F('amount') - F('paid_amount')))[
    #         'total'] or 0
    #     return charges_balance

    @property
    def interest_amount(self):
        # get all interest
        total_interest = self.installments.aggregate(total=Sum('interest'))[
            'total'] or 0
        total_interest = int(round(total_interest, -2))
        return total_interest

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
            total_amount = F('principal') + F('interest')
            paid_amount = F('paid_amount')
            overdue_amount = self.installments.filter(status__in=[OVERDUE, MISSED]).aggregate(
                # calculate the installment balance
                total=Sum(total_amount - paid_amount))['total'] or 0
            return overdue_amount

    @property
    def progress(self):
        if self.amount_paid and self.payment_amount:
            completion = self.amount_paid / self.payment_amount * 100
            return int(completion)

    @property
    def next_payment_date(self):
        # Filter installments to get those that are pending or not paid
        next_installment = self.installments.filter(
            # Adjust status field names as per your model
            status__in=[NOT_PAID, PARTIALLY_PAID],
            due_date__gt=now()  # Filter installments with due dates in the future
        ).order_by('due_date').first()

        return next_installment.due_date if next_installment else None

    # mapping for the importer

    def get_field_mapping(self):
        return {
            # 'client': 'client',
            'category': 'category',
            'loan_term': 'loan_term',
            'interest_rate': 'interest_rate',
            'amount': 'amount',
            'payment_frequency': 'payment_frequency',
        }

    class Meta:
        ordering = ['-created_at']
        permissions = (
            ("can_change_loan_status", "Can change loan status"),
        )

    def __str__(self):
        return f'{self.ref_number} - {self.amount}'
