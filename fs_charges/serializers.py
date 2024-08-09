
from fs_charges.models import *
from fs_utils.serializers import BaseSerializer
from rest_framework import serializers


class ChargeSerializer(BaseSerializer):
    class Meta:
        model = Charge
        fields = '__all__'


class ChargePenaltySerializer(BaseSerializer):
    balance = serializers.IntegerField(read_only=True)

    class Meta:
        model = ChargePenalty
        fields = '__all__'
