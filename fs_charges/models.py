from django.db import models
from fs_utils.models import BaseModel


class Charge(BaseModel):
    name = models.CharField(max_length=100)
    charge = models.DecimalField(
        max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.name} ({self.charge}%)'
