from rest_framework import serializers

from fs_utils.constants import DISBURSEMENT

from .models import *
from fs_utils.serializers import BaseSerializer


class TransactionSerializer(BaseSerializer):

    ref_number = serializers.CharField(
        source="loan.ref_number", read_only=True)

    client_name = serializers.CharField(
        source="loan.client.display_name", read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


def create_transaction(self, validated_data, instance):
    # get transaction type
    transaction_type = validated_data.pop('transaction_type', None)

    # create transaction
    if transaction_type == DISBURSEMENT:
        Transaction.objects.create(
            loan=instance,
            amount=instance.amount,
            type=DISBURSEMENT,
            comment="System generated transaction",
            created_by=self.context['request'].user
        )
