from rest_framework import serializers

from .models import LoanPayment
from fs_utils.serializers import BaseSerializer


class LoanPaymentSerializer(BaseSerializer):

    borrower_name = serializers.CharField(
        source="loan.borrower_name", read_only=True)

    class Meta:
        model = LoanPayment
        fields = '__all__'

    # def create(self, validated_data):
    #     validated_data['payment_number'] = generate_unique_number("LP")
    #     return super().create(validated_data)
