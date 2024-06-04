from rest_framework import serializers

from fs_utils.serializers import CreateCurrentUser, SimpleUser
from .models import LoanReport


class LoanReportSerializer(serializers.ModelSerializer):

    created_by = SimpleUser(
        required=False, default=CreateCurrentUser(),
    )

    class Meta:
        model = LoanReport
        fields = '__all__'
