from django.db import models
from fs_audits.models import AuditTrail
from fs_loans.models import Loan
from fs_utils.constants import DATE_FORMAT, INSTALLMENT_CHOICES, LOAN, NOT_PAID, REPAYMENT
from fs_utils.models import BaseModel

# Create your models here.


class Installment(BaseModel):
    loan = models.ForeignKey(
        Loan, on_delete=models.DO_NOTHING, related_name='installments')
    interest = models.IntegerField(default=0)
    due_date = models.DateField()
    principal = models.PositiveIntegerField()
    paid_amount = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=INSTALLMENT_CHOICES, default=NOT_PAID)
    payment_date = models.DateTimeField(blank=True, null=True)
    # fees = models.IntegerField(default=0)
    # penalty = models.IntegerField(default=0)

    class Meta:
        ordering = ['due_date']

    # update loan due date
    def save(self, *args, update_loan=True, **kwargs):
        # AUDIT TRAIL
        AuditTrail.objects.create(
            action=REPAYMENT,
            model_name=LOAN,
            object_id=self.loan.pk,
            actor=self.updated_by,
            changes={'total_amount': self.total_amount,
                     'paid_amount': self.paid_amount, 'status': self.status, 'due_date': self.due_date.strftime(DATE_FORMAT)}
        )
        super().save(*args, **kwargs)
        # update loan due date
        if update_loan:
            self.loan.update_due_date()

    @property
    def total_amount(self):
        return self.principal + self.interest

    @property
    def balance(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f'Installment {self.id} for {self.loan.ref_number} - {self.status}, Balance: {self.balance}'
