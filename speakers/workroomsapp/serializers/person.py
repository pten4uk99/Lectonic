from rest_framework import serializers

from workroomsapp.models import Person


class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [

        ]

