from .models import *
from fs_utils.serializers import BaseSerializer
from rest_framework import serializers


class CategorySerializer(BaseSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')
