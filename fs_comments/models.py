from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from fs_audits.models import AuditTrail
from fs_utils.constants import COMMENT
from fs_utils.models import BaseModel

# Create your models here.


class Comment(BaseModel):
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # AUDIT TRAIL COMMENT
        AuditTrail.objects.create(
            action=COMMENT,
            model_name=self.content_type.model,  # model name
            object_id=self.object_id,
            actor=self.created_by,
            changes={'comment': self.comment},
        )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.comment
