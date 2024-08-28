from django.db import models
from fs_audits.models import AuditTrail
from fs_loans.models import Loan
from fs_utils.constants import CHARGE, CHARGE_CHOICES, CHARGE_PENALTY_CHOICES, LOAN, NOT_PAID
from fs_utils.models import BaseModel


class Charge(BaseModel):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=CHARGE_CHOICES)
    description = models.TextField(max_length=250, null=True, blank=True)

    def get_field_mapping(self):
        return {
            'name': 'name',
            'amount': 'amount',
            'type': 'type',
            'description': 'description',
        }

    def __str__(self):
        return f'{self.name} ({self.amount})'


class ChargePenalty(BaseModel):
    loan = models.ForeignKey(
        Loan, on_delete=models.DO_NOTHING, related_name='charge_penalties')
    type = models.CharField(max_length=10, choices=CHARGE_CHOICES)
    amount = models.PositiveIntegerField()
    comment = models.TextField(max_length=1000, null=True, blank=True)
    paid_amount = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=CHARGE_PENALTY_CHOICES, default=NOT_PAID)
    payment_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, is_update=False, **kwargs):
        super().save(*args, **kwargs)

        changes = {'type': self.type,
                   'amount': self.amount, 'status': self.status}

        if is_update:
            changes = {'type': self.type, 'amount': self.amount,
                       'paid_amount': self.paid_amount, 'status': self.status}

        # Create Audit for transaction on loan
        AuditTrail.objects.create(
            action=CHARGE,
            model_name=LOAN,
            object_id=self.loan.pk,
            actor=self.created_by,
            changes=changes,
        )

    @property
    def balance(self):
        return self.amount - self.paid_amount

    def __str__(self):
        return f'{self.loan.ref_number} - {self.type} - {self.amount}  - Balance: {self.balance}'
