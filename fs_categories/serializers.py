from fs_documents.serializers import DocumentSerializer
from .models import *
from fs_utils.serializers import BaseSerializer


class CategorySerializer(BaseSerializer):

    attachments = DocumentSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'
