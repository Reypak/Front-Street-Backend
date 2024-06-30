from fs_documents.serializers import DocumentSerializer
from .models import *
from fs_utils.serializers import BaseSerializer
from rest_framework import serializers


class CategorySerializer(BaseSerializer):

    attachments = DocumentSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')
