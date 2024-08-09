from rest_framework import serializers

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
