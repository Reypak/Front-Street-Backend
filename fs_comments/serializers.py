from rest_framework import serializers

from fs_utils.serializers import BaseSerializer
from .models import Comment
from django.contrib.contenttypes.models import ContentType


class CommentSerializer(BaseSerializer):
    content_type = serializers.CharField(write_only=True)
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at',
                  'created_by', 'content_type', 'object_id']

    def create(self, validated_data):

        content_type_str = validated_data.pop('content_type')
        try:
            # get the content_type instance
            content_type = ContentType.objects.get(model=content_type_str)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content type")

        validated_data['content_type'] = content_type
        return super().create(validated_data)


def create_comment(validated_data, instance):
    # get comment text
    comment = validated_data.pop('comment', None)

    # create comment
    if comment is not None:
        Comment.objects.create(
            comment=comment,
            content_object=instance
        )
