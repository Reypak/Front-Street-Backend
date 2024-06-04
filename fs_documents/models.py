from django.db import models
from fs_utils.constants import DOCUMENT_TYPES
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Document(models.Model):
    caption = models.CharField(max_length=100, null=False, blank=False)
    file = CloudinaryField(resource_type='raw', default=None,
                           null=True, blank=True, folder="media")
    document_type = models.CharField(
        max_length=100,
        choices=DOCUMENT_TYPES,
        default="attachment",
        null=False,
        blank=False
    )

    def __str__(self):
        return self.caption + ' - '+self.document_type
