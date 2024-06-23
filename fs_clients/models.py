# Create your models here.
from fs_utils.models import BaseModel
from django.db import models


class Client(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
