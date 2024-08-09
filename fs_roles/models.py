from django.db import models
from django.contrib.auth.models import Permission
from fs_api import settings

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="%(class)s_created_by")
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="%(class)s_updated_by")

    class Meta:
        permissions = (
            ("can_admin", "Can admin"),
            ("can_public", "Can public"),
        )

    def __str__(self):
        return self.name
