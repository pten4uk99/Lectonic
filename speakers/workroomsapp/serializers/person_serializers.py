import re
import datetime

from rest_framework import serializers

from workroomsapp.models import Person, City, DocumentImage, Image


class PersonSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Person
        exclude = [
            'id',
            'rating',
            'sys_created_at',
            'sys_modified_at',
            'is_lecturer',
            'is_project_admin',
            'is_customer',
            'is_verified'
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
        return self.name_validator(middle_name)

    def validate_birth_date(self, birth_date):
        '''
        1. Дата не может быть позже сегодняшней
        '''

        if birth_date > datetime.date.today():
            raise serializers.ValidationError('Дата не может быть позже текущей')

        return birth_date


class DocumentImageSerializer(serializers.Serializer):
    passport = serializers.FileField()
    selfie = serializers.FileField()

    class Meta:
        model = DocumentImage
        fields = [
            'passport',
            'selfie'
        ]

    def create(self, validated_data):
        return DocumentImage.objects.create(
            person=Person.objects.first(),
            passport=Image.objects.create(photo=validated_data['passport']),
            selfie=Image.objects.create(photo=validated_data['selfie']),
        )


class CitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(error_messages={'required': 'Обязательное поле'})

    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'region'
        ]
