from django.db import models
from fs_documents.models import Document
from fs_utils.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    attachments = models.ManyToManyField(Document, blank=True)

    def __str__(self):
        return self.name
