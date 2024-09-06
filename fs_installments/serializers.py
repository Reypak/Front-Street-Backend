from fs_utils.serializers import BaseSerializer
from .models import Installment
from rest_framework import serializers


class InstallmentSerializer(BaseSerializer):
    total_amount = serializers.IntegerField(read_only=True)
    balance = serializers.IntegerField(read_only=True)
    ref_number = serializers.CharField(
        source='loan.ref_number', read_only=True)
    loan_status = serializers.CharField(
        source='loan.status', read_only=True)

    class Meta:
        model = Installment
        fields = '__all__'


class RescheduleSerializer(serializers.Serializer):
    loan = serializers.IntegerField(required=True)
    loan_term = serializers.IntegerField(min_value=1, required=True)
    # interest_rate = serializers.DecimalField(
    #     max_digits=5, decimal_places=2, required=True)
    amount = serializers.IntegerField(required=True)
    start_date = serializers.DateField(required=True)
