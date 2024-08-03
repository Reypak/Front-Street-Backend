import json
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from fs_audits.models import AuditTrail


class AuditTrailMixin(models.Model):
    class Meta:
        abstract = True

    def get_original_data(self):
        if self.pk:
            original_data = self.__class__.objects.get(pk=self.pk)
        else:
            original_data = None
        return original_data


@receiver(pre_save)
def track_changes(sender, instance, **kwargs):
    if not issubclass(sender, AuditTrailMixin):
        return

    if not instance.pk:
        instance._action = 'create'
        instance._changes = {field.name: serialize_field(
            getattr(instance, field.name)) for field in instance._meta.fields}
    else:
        instance._action = 'update'
        instance._changes = {}
        original = instance.get_original_data()
        if original is not None:
            for field in instance._meta.fields:
                field_name = field.name
                # serialize object fields
                original_value = serialize_field(getattr(original, field_name))
                new_value = serialize_field(getattr(instance, field_name))
                # compare old and new values
                if original_value != new_value:
                    instance._changes[field_name] = {
                        'old': original_value,
                        'new': new_value
                    }


@receiver(post_save)
def save_audit_trail(sender, instance, **kwargs):
    if not issubclass(sender, AuditTrailMixin):
        return

    action = getattr(instance, '_action', 'update')
    changes = getattr(instance, '_changes', {})

    AuditTrail.objects.create(
        action=action,
        model_name=sender.__name__,
        object_id=instance.pk,
        actor=getattr(instance, 'updated_by', None),
        changes=changes
    )


@receiver(post_delete)
def delete_audit_trail(sender, instance, **kwargs):
    if not issubclass(sender, AuditTrailMixin):
        return

    AuditTrail.objects.create(
        action='delete',
        model_name=sender.__name__,
        object_id=instance.pk,
        actor=getattr(instance, 'updated_by', None),
        changes={}
    )


def serialize_field(value):
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    return str(value)
