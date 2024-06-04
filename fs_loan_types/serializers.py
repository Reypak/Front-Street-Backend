from rest_framework import serializers
from .models import LoanType
from utils.serializers import CreateCurrentUser, SimpleUser


class LoanTypeSerializer(serializers.ModelSerializer):

    created_by = SimpleUser(
        required=False, default=CreateCurrentUser(),
    )

    class Meta:
        model = LoanType
        fields = '__all__'

        # read_only_fields = ['created_by']
        # fields = ['id', 'borrower_name', 'phone', 'amount', 'status']
