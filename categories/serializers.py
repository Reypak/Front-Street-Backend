from rest_framework import serializers
from .models import Category
from utils.serializers import CreateCurrentUser, SimpleUser


class CategorySerializer(serializers.ModelSerializer):

    created_by = SimpleUser(
        required=False, default=CreateCurrentUser(),
    )

    class Meta:
        model = Category
        fields = '__all__'

        # read_only_fields = ['created_by']
        # fields = ['id', 'borrower_name', 'phone', 'amount', 'status']
