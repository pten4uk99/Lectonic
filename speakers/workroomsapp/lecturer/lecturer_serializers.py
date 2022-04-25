from rest_framework import serializers

from speakers.settings import DEFAULT_HOST
from workroomsapp.models import Lecturer, DiplomaImage, Domain
from workroomsapp.person.person_serializers import PersonSerializer


class DiplomaImageCreateSerializer(serializers.Serializer):
    diploma = serializers.FileField()

    class Meta:
        fields = ['diploma']

    def validate_diploma(self, diploma):
        lecturer = self.context['request'].user.person.lecturer

        if lecturer.diploma_images.all().count() >= 5:
            msg = 'Превышено максимальное количество дипломов (5)'
            raise serializers.ValidationError(msg)

        image_format = diploma.name.split('.')[-1]
        diploma.name = 'diploma.' + image_format
        return diploma

    def create(self, validated_data):
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
        for name in domain:
            if not Domain.objects.filter(name=name).exists():
                raise serializers.ValidationError('Данной тематики не существует')
        return domain

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


class LecturersListGetSerializer(serializers.ModelSerializer):
    first_name = serializers.StringRelatedField(source='person.first_name')
    last_name = serializers.StringRelatedField(source='person.last_name')
    middle_name = serializers.StringRelatedField(source='person.middle_name')
    bgc_number = serializers.StringRelatedField(source='person.bgc_number')
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Lecturer
        fields = [
            'id',
            'photo',
            'first_name',
            'last_name',
            'middle_name',
            'bgc_number'
        ]

    def get_photo(self, obj):
        if obj.person.photo:
            return DEFAULT_HOST + obj.person.photo.url
        else:
            return ''


class LecturerGetSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    domain = serializers.SerializerMethodField()
    optional = serializers.SerializerMethodField()
    performances_links = serializers.SerializerMethodField()
    publication_links = serializers.SerializerMethodField()

    class Meta:
        model = Lecturer
        fields = [
            'id',
            'person',
            'performances_links',
            'publication_links',
            'education',
            'optional',
            'domain',
        ]

    def get_optional(self, lecturer):
        return {
            'hall_address': lecturer.optional.hall_address,
            'equipment': lecturer.optional.equipment
        }

    def get_performances_links(self, lecturer):
        return lecturer.performances_links.all().values_list('url', flat=True)

    def get_publication_links(self, lecturer):
        return lecturer.publication_links.all().values_list('url', flat=True)

    def get_domain(self, lecturer):
        return lecturer.lecturer_domains.all().values_list('domain__name', flat=True)
