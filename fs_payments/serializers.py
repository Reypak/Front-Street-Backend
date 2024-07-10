from rest_framework import serializers

from .models import LoanPayment
from fs_utils.serializers import BaseSerializer


class LoanPaymentSerializer(BaseSerializer):

    ref_number = serializers.CharField(
        source="loan.ref_number", read_only=True)

    client_name = serializers.CharField(
        source="loan.client.display_name", read_only=True)

    class Meta:
        model = LoanPayment
        fields = '__all__'

    # def create(self, validated_data):
    #     validated_data['payment_number'] = generate_unique_number("LP")
    #     return super().create(validated_data)
