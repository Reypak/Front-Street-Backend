
from rest_framework import serializers
from fs_tasks.models import Task
from fs_users.models import CustomUser
from fs_utils.serializers import BaseSerializer, SimpleUser
from django.contrib.contenttypes.models import ContentType


class TaskSerializer(BaseSerializer):
    assignees = SimpleUser(many=True, read_only=True)
    assignees_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all(), write_only=True, source='assignees'
    )

    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model'
    )

    class Meta:
        model = Task
        fields = '__all__'
