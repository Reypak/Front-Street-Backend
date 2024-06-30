from .models import Installment
from rest_framework import serializers


class InstallmentSerializer(serializers.ModelSerializer):
    total_amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Installment
        fields = '__all__'
