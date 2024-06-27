from rest_framework import serializers
from django.contrib.auth import get_user_model


# Simple user class inheritable
class SimpleUser(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "id"
        ]


class CreateCurrentUser(serializers.CurrentUserDefault):

    def set_context(self, serializer_field):
        self.is_update = serializer_field.parent and serializer_field.parent.instance is not None


class BaseSerializer(serializers.ModelSerializer):
    created_by = SimpleUser(
        required=False, default=CreateCurrentUser(),
    )

    class Meta:
        abstract = True
