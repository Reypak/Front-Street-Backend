from rest_framework import serializers
from django.db import models
from fs_categories.serializers import CategoryDetailsSerializer, CategorySerializer
from fs_documents.helpers import save_attachments
from fs_documents.models import Document
from fs_documents.serializers import DocumentSerializer
from .models import Loan
from fs_utils.serializers import BaseSerializer, ClientSerializer


class LoanSerializer(BaseSerializer):

    class Meta:
        model = Loan
        fields = '__all__'

    def create(self, validated_data):
        # Extract and remove 'attachments' from validated_data
        attachments_data = validated_data.pop('attachments', [])

        # Create the Loan object
        instance = super(LoanSerializer, self).create(validated_data)

        # create application number
        instance.ref_number = f"FS/LOA/{instance.id}"
        instance.save()

        # Create Document objects
        attachments = [Document.objects.create(
            **data) for data in attachments_data]

        # Associate the created Document objects with the Loan object
        instance.attachments.set(attachments)

        return instance

    def update(self, instance, validated_data):

        # get updating user
        # instance.updated_by = self.context['request'].user

        save_attachments(instance, validated_data)

        return super(LoanSerializer, self).update(instance, validated_data)


class LoanListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name", read_only=True)

    client = serializers.CharField(
        source="client.first_name", read_only=True)

    class Meta:
        model = Loan
        fields = ('id', 'ref_number',
                  'amount', 'status', 'created_at', 'category_name', 'client')


class LoanViewSerializer(BaseSerializer):

    # Get field name from category attribute
    category_name = serializers.CharField(
        source="category.name", read_only=True)

    attachments = DocumentSerializer(many=True, required=False)

    client = ClientSerializer()

    class Meta:
        model = Loan
        fields = '__all__'

    outstanding_balance = serializers.IntegerField()

    payment_amount = serializers.IntegerField()

    amount_paid = serializers.IntegerField()

    category = CategoryDetailsSerializer()

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Iterate through the payments
    #     total_payments = instance.payments.aggregate(
    #         total=models.Sum('amount_paid'))['total'] or 0
    #     # set outstanding_balance
    #     data['outstanding_balance'] = instance.amount - total_payments
    #     return data
