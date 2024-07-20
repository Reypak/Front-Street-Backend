from django.db import models
from fs_users.models import CustomUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True  # Set this model as Abstract to allow inheritance
