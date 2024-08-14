from django.db import models

from fs_users.models import CustomUser

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE)
    is_employed = models.BooleanField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} - Profile'
