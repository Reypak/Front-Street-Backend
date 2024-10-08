from django.db import models
from fs_loans.models import Loan

from fs_users.models import CustomUser

# Create your models here.


class LoanReport(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Loan ({self.loan.id}) {self.action} - {self.status} - {self.created_by.display_name}'
