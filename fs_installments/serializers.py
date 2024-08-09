from fs_utils.serializers import BaseSerializer
from .models import Installment
from rest_framework import serializers


class InstallmentSerializer(BaseSerializer):
    total_amount = serializers.IntegerField(read_only=True)
    balance = serializers.IntegerField(read_only=True)

    class Meta:
        model = Installment
        fields = '__all__'
