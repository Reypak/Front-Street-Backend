from django.db import models
from utils.models import BaseModel


class LoanType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.name
