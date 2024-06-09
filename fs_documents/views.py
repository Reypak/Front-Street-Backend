from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
