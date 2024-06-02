from rest_framework import serializers

from documents.helpers import save_attachments
from documents.models import Document
from documents.serializers import DocumentSerializer
from .models import Loan
from utils.serializers import CreateCurrentUser, SimpleUser


class LoanSerializer(serializers.ModelSerializer):

    created_by = SimpleUser(
        required=False, default=CreateCurrentUser(),
    )

    # Get field name from category attribute
    category_name = serializers.CharField(
        source="category.name", read_only=True)

    attachments = DocumentSerializer(many=True)

    class Meta:
        model = Loan
        fields = '__all__'

    # def create(self, validated_data):
    #     loan = Loan.objects.create(**validated_data)

    #     attachments_data = validated_data.pop('attachments')
    #     for attachment_data in attachments_data:
    #         attachment = Document.objects.create(**attachment_data)
    #         loan.attachments.add(attachment)
    #     return loan
        # return super(LoanSerializer, self).create(instance, validated_data)

    def create(self, validated_data):
        # Extract and remove 'attachments' from validated_data
        attachments_data = validated_data.pop('attachments', [])

        # Create the Loan object
        instance = super(LoanSerializer, self).create(validated_data)

        # Create Document objects
        attachments = [Document.objects.create(
            **data) for data in attachments_data]

        # Associate the created Document objects with the Loan object
        instance.attachments.set(attachments)

        return instance

    def update(self, instance, validated_data):

        # instance.borrower_name = validated_data.get(
        #     'borrower_name', instance.borrower_name)
        # instance.amount = validated_data.get(
        #     'amount', instance.amount)
        # instance.save()

        save_attachments(instance, validated_data)

        return super(LoanSerializer, self).update(instance, validated_data)
