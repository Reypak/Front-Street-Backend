from .models import Installment
from rest_framework import serializers


class InstallmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Installment
        fields = '__all__'
