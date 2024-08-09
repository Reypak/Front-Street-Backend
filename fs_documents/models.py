from django.db import models
from fs_utils.constants import DOCUMENT_TYPE_ATTACHMENT, DOCUMENT_TYPES
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Document(models.Model):
    caption = models.CharField(max_length=100, null=True, blank=True)
    file = CloudinaryField(resource_type='raw', default=None,
                           null=True, blank=True, folder="media")
    document_type = models.CharField(
        max_length=100,
        choices=DOCUMENT_TYPES,
        default=DOCUMENT_TYPE_ATTACHMENT,
        null=False,
        blank=False
    )

    def __str__(self):
        return f'{self.caption} - {self.document_type}'
