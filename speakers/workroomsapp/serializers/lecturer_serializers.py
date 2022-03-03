from rest_framework import serializers

from workroomsapp.models import Lecturer, Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['url']


class DomainSerializer(serializers.ModelSerializer):
    pass


class LecturerCreateSerializer(serializers.Serializer):
    person = serializers.HiddenField(default=serializers.CurrentUserDefault())
    domain = serializers.ListField()
    performances_links = serializers.ListField()
    publication_links = serializers.ListField()
    diploma_image = serializers.ImageField()
    education = serializers.CharField()
    passport = serializers.ImageField()
    selfie = serializers.ImageField()
    hall_address = serializers.CharField(max_length=200)
    equipment = serializers.CharField(max_length=500)

    class Meta:
        model = Lecturer
        fields = [
            'person',
            'domain',
            'performances_links',
            'publication_links',
            'diploma_image',
            'education',
            'hall_address',
            'equipment'
        ]
