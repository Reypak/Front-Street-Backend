from django.db import models

from fs_users.models import CustomUser
from fs_utils.constants import ACTION_CHOICES


class AuditTrail(models.Model):

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    changes = models.JSONField()

    # class Meta:
    # ordering=['-id']
    # verbose_name = 'Audit Trail'
    # verbose_name_plural = 'Audit Trails'

    def __str__(self):
        return f'{self.action} on {self.model_name} id {self.object_id} by {self.actor}'
