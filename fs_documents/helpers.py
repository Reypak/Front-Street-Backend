from .models import Document


def save_attachments(instance, validated_data):
    if 'attachments' in validated_data:
        attachments_data = validated_data.pop('attachments')

        for attachment_data in attachments_data:
            attachment = Document.objects.create(
                **attachment_data)
            instance.attachments.add(attachment)
