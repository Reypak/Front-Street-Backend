from django.db import models
from fs_loans.models import Loan
from django.contrib.auth.models import User

# Create your models here.


class LoanReport(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Loan {self.loan.id} - {self.status} - {self.created_by.username}'
