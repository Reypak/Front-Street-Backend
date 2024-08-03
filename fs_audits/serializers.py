from rest_framework import serializers
from .models import AuditTrail


class AuditTrailSerializer(serializers.ModelSerializer):
    # To display the username instead of the user id

    actor_name = serializers.CharField(
        source="actor.display_name", read_only=True)

    class Meta:
        model = AuditTrail
        fields = '__all__'
