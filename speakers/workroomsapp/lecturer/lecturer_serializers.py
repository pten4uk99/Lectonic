from rest_framework import serializers

from workroomsapp.models import Lecturer, Link, Person, DiplomaImage


class DiplomaImageCreateSerializer(serializers.Serializer):
    diploma = serializers.FileField()

    class Meta:
        fields = ['diploma']

    def validate_diploma(self, diploma):
        image_format = diploma.name.split('.')[-1]

        if image_format not in ['jpg', 'jpeg', 'png']:
            msg = 'Диплом может быть только в формате "jpg", "jpeg" или "png"'
            raise serializers.ValidationError(msg)

        diploma.name = 'diploma.' + image_format

        return diploma

    def create(self, validated_data):
        DiplomaImage.objects.all().delete()  # ТОЛЬКО В РЕЖИМЕ РАЗРАБОТКИ!!!
        return DiplomaImage.objects.create(
            lecturer=self.context['request'].user.person.lecturer,
            diploma=validated_data['diploma']
        )


class DiplomaImageGetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DiplomaImage
        fields = ['diploma']


class LecturerCreateSerializer(serializers.Serializer):
    domain = serializers.ListField()
    performances_links = serializers.ListField(required=False)
    publication_links = serializers.ListField(required=False)
    education = serializers.CharField(required=False)
    hall_address = serializers.CharField(max_length=200, required=False)
    equipment = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = [
            'domain',
            'performances_links',
            'publication_links',
            'education',
            'hall_address',
            'equipment'
        ]

    def validate_domain(self, domain):
        try:
            validated_domain = list(map(int, domain))
        except ValueError:
            raise serializers.ValidationError('Тематика должна быть числом')

        return validated_domain

    def create(self, validated_data):
        return Lecturer.objects.create_lecturer(
            person=self.context['request'].user.person,
            performances_links=validated_data.get('performances_links'),
            publication_links=validated_data.get('publication_links'),
            domain=validated_data.get('domain'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            education=validated_data.get('education')
        )

