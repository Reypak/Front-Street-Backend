from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from fs_tasks.filters import TaskFilterSet
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilterSet

    def perform_update(self, serializer):
        return serializer.save(updated_by=self.request.user)

    # def get_queryset(self):
    #     id = self.request.query_params.get('id')
    #     model = self.request.query_params.get('type')

    #     if id is not None:
    #         return Task.objects.filter(fields__icontains=f'"{model}": {id}')

    def get_queryset(self):
        model = self.request.query_params.get('type')

        # get all tasks for loan
        if model is not None:
            queryset = Task.objects.all()
        else:
            # get all tasks for the user
            queryset = Task.objects.filter(assignees=self.request.user)

        # Allow all users to retrieve any task
        if self.action == 'retrieve':
            return Task.objects.all()

        return queryset.order_by('-created_at')
