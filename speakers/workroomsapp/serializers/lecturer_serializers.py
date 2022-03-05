from rest_framework import serializers

from workroomsapp.models import Lecturer, Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['url']


class DomainSerializer(serializers.ModelSerializer):
    pass


class LecturerCreateSerializer(serializers.Serializer):
    # person = serializers.HiddenField(default=serializers.CurrentUserDefault())
    person = serializers.IntegerField()
    domain = serializers.ListField()
    performances_links = serializers.ListField(required=False)
    publication_links = serializers.ListField(required=False)
    diploma_image = serializers.ImageField(required=False)
    education = serializers.CharField(required=False)
    # passport = serializers.ImageField()
    # selfie = serializers.ImageField()
    hall_address = serializers.CharField(max_length=200, required=False)
    equipment = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = [
            'person',
            'domain',
            'performances_links',
            'publication_links',
            'diploma_image',
            'education',
            # 'passport',
            # 'selfie',
            'hall_address',
            'equipment'
        ]

    def create(self, validated_data):
        return Lecturer.objects.create_lecturer(
            person=self.context['request']['user'].person,
            performances_links=validated_data.get('performances_links'),
            publication_links=validated_data.get('publication_links'),
            domain=validated_data.get('domain'),
            diploma_image=validated_data.get('diploma_image'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            education=validated_data.get('education')
        )


