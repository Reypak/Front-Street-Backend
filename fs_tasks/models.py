from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from fs_users.models import CustomUser
from fs_utils.constants import PENDING, TASK_STATUS_CHOICES
from fs_utils.models import BaseModel

# Create your models here.


class Task(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    assignees = models.ManyToManyField(CustomUser, related_name='tasks')
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=TASK_STATUS_CHOICES, default=PENDING)
    # ForeignKey to the specific loan or application based on task_type
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title
