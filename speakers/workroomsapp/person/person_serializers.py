import re
import datetime

from django.core.files.storage import default_storage
from rest_framework import serializers

from workroomsapp.models import Person, City, Domain


class PersonPhotoGetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ['photo']


class PersonSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    photo = serializers.FileField(required=False)

    class Meta:
        model = Person
        exclude = [
            'is_lecturer',
            'is_customer',
            'is_verified',
            'rating',
            'is_project_admin',
            'sys_created_at',
            'sys_modified_at'
        ]

    def name_validator(self, name):
        '''
        Общий валидатор для имени, фамилии и отчества.

        1. Все буквы должны быть кириллицей
        2. Первая буква имени должна быть заглвной
        3. Затем может быть сколько угодно строчных символов без пробелов

        '''

        match = re.findall(r'^[А-Яа-яё-]+$', name)

        if not match:
            raise serializers.ValidationError('Неверный формат имени')

        return name

    def validate_first_name(self, first_name):
        return self.name_validator(first_name)

    def validate_last_name(self, last_name):
        return self.name_validator(last_name)

    def validate_middle_name(self, middle_name):
        if not middle_name:
            return middle_name
        return self.name_validator(middle_name)

    def validate_birth_date(self, birth_date):
        '''
        1. Дата не может быть позже сегодняшней
        '''

        if birth_date > datetime.date.today():
            raise serializers.ValidationError('Дата не может быть позже текущей')

        return birth_date

    def validate_photo(self, photo):
        image_format = photo.name.split('.')[-1]
        photo.name = 'photo.' + image_format
        return photo

    def update(self, instance, validated_data):
        if 'photo' in validated_data and instance.photo:
            default_storage.delete(instance.photo.path)
        return super().update(instance, validated_data)


class CitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(error_messages={'required': 'Обязательное поле'})

    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'region'
        ]


class DomainGetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(error_messages={'required': 'Обязательное поле'})

    class Meta:
        model = Domain
        fields = [
            'id',
            'name'
        ]
