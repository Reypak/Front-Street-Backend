from django.db import models
from utils.models import BaseModel
from cloudinary.models import CloudinaryField
from categories.models import Category


class Loan(BaseModel):
    # id = models.AutoField(primary_key=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    borrower_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=500)
    amount = models.IntegerField()
    status = models.CharField(max_length=50, default='pending')
    attachment = CloudinaryField(resource_type='raw', default=None,
                                 null=True, blank=True, folder="media")

    def __str__(self):
        return self.borrower_name + ' - ' + str(self.amount) + ' - ' + str(self.category)
