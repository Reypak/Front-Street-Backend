from rest_framework import serializers
from fs_categories.serializers import CategoryDetailsSerializer
from fs_comments.serializers import create_comment
from fs_documents.helpers import save_attachments
from fs_documents.models import Document
from fs_documents.serializers import DocumentSerializer
from .models import Loan
from fs_utils.serializers import BaseSerializer, ClientSerializer


class LoanSerializer(BaseSerializer):

    comment = serializers.CharField(write_only=True, required=False)

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

        # handle comments
        create_comment(self=self, validated_data=validated_data,
                       instance=instance)

        # get updating user
        # instance.updated_by = self.context['request'].user

        save_attachments(instance, validated_data)

        return super(LoanSerializer, self).update(instance, validated_data)


class LoanListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name", read_only=True)

    client_name = serializers.CharField(
        source="client.display_name", read_only=True)

    class Meta:
        model = Loan
        fields = ('id', 'ref_number',
                  'amount', 'status', 'created_at', 'category_name', 'client_name')


class LoanViewSerializer(BaseSerializer):

    # Get field name from category attribute
    # category_name = serializers.CharField(
    #     source="category.name", read_only=True)

    attachments = DocumentSerializer(many=True, required=False)
    client_details = ClientSerializer(source="client")
    overdue = serializers.IntegerField()
    interest_amount = serializers.IntegerField()
    outstanding_balance = serializers.IntegerField()
    payment_amount = serializers.IntegerField()
    amount_paid = serializers.IntegerField()
    charges = serializers.IntegerField()
    category_details = CategoryDetailsSerializer(source="category")
    application_number = serializers.CharField(source="application")

    class Meta:
        model = Loan
        fields = '__all__'

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Iterate through the payments
    #     total_payments = instance.payments.aggregate(
    #         total=models.Sum('amount_paid'))['total'] or 0
    #     # set outstanding_balance
    #     data['outstanding_balance'] = instance.amount - total_payments
    #     return data
