from rest_framework import generics
# from fs_comments.filters import CommentFilterSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    # filterset_class = CommentFilterSet

    def get_queryset(self):
        object_id = self.kwargs['pk']
        content_type = self.request.query_params.get('type')
        return Comment.objects.filter(content_type__model=content_type, object_id=object_id)
