from rest_framework import serializers
from .models import Loan
from utils.serializers import CreateCurrentUser, SimpleUser


class LoanSerializer(serializers.ModelSerializer):

    created_by = SimpleUser(
        required=False, default=CreateCurrentUser(),
    )

    class Meta:
        model = Loan
        fields = '__all__'

        # read_only_fields = ['created_by']
        # fields = ['id', 'borrower_name', 'phone', 'amount', 'status']
