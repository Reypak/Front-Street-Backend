from django.db import models
from fs_utils.models import BaseModel
from django.core.validators import MinValueValidator


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    max_amount = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(10000)])
    is_active = models.BooleanField(default=True)
    document_fields = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
