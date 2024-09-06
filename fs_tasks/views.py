from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from fs_tasks.filters import TaskFilterSet
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilterSet

    # def get_queryset(self):
    #     id = self.request.query_params.get('id')
    #     model = self.request.query_params.get('type')

    #     if id is not None:
    #         return Task.objects.filter(fields__icontains=f'"{model}": {id}')
