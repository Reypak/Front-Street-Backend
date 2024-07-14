from django.db import models
from django.contrib.auth.models import Permission

# from fs_users.models import CustomUser

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    # created_by = models.ForeignKey(
    #     CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
