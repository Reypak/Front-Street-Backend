from rest_framework import serializers
from django.contrib.auth import get_user_model

from fs_profiles.serializer import ProfileSerializer
from fs_users.models import CustomUser


# Simple user class inheritable
class SimpleUser(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'display_name',
            "email",
        ]


class CreateCurrentUser(serializers.CurrentUserDefault):

    def set_context(self, serializer_field):
        self.is_update = serializer_field.parent and serializer_field.parent.instance is not None


class BaseSerializer(serializers.ModelSerializer):
    created_by = SimpleUser(
        required=False, default=CreateCurrentUser(),
    )
    updated_by = SimpleUser(
        required=False, default=CreateCurrentUser(),
    )

    class Meta:
        abstract = True


class ClientSerializer(BaseSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'profile',
            'display_name',
            'email',
            'phone_number',)
