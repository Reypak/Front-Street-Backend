

from fs_applications.models import Application
from fs_documents.helpers import save_attachments
from fs_documents.models import Document
from fs_documents.serializers import DocumentSerializer
from fs_utils.serializers import BaseSerializer
from rest_framework import serializers


class ApplicationSerializer(BaseSerializer):

    loan_category_name = serializers.CharField(
        source="loan_category.name", read_only=True)

    attachments = DocumentSerializer(many=True)

    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        # Extract and remove 'attachments' from validated_data
        attachments_data = validated_data.pop('attachments', [])

        # Create the Loan object
        instance = super(ApplicationSerializer, self).create(validated_data)

        # create application number
        instance.ref_number = f"FS/APP/{instance.id}"
        instance.save()

        # Create Document objects
        attachments = [Document.objects.create(
            **data) for data in attachments_data]

        # Associate the created Document objects with the Loan object
        instance.attachments.set(attachments)

        return instance

    def update(self, instance, validated_data):

        save_attachments(instance, validated_data)

        return super(ApplicationSerializer, self).update(instance, validated_data)
