from emailapp.models import EmailConfirmation
from rest_framework import serializers

class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmation
        fields = (
            'email',
        )