import re
import datetime

from rest_framework import serializers

from workroomsapp.models import Person, City


class PersonCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False)
    birth_date = serializers.DateField()
    city = serializers.CharField(max_length=100)  # Пока что ввод города вручную, позже переделать на PrimaryKeyRelatedField()
    # address = serializers.CharField(max_length=200, required=False)
    rating = serializers.IntegerField(required=False)
    # photo = serializers.CharField(max_length=200, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # grade = serializers.CharField(max_length=300, default='', required=False)
    description = serializers.CharField(required=False)
    # domain = serializers.PrimaryKeyRelatedField(queryset=Domain.objects.all(), required=False)
    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=7,
        required=False
    )
    longitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=7,
        required=False
    )

    class Meta:
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'birth_date',
            'city',
            # 'address',
            'rating',
            # 'photo',
            'user',
            # 'grade',
            'description',
            # 'domain',
            'latitude',
            'longitude',
        ]

    def name_validator(self, name):
        '''
        Общий валидатор для имени, фамилии и отчества.

        1. Все буквы должны быть кириллицей
        2. Первая буква имени должна быть заглвной
        3. Затем может быть сколько угодно строчных символов без пробелов

        '''

        match = re.findall(r'^[A-Я][а-я]+$', name)

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

    def validate_city(self, city):
        match = re.findall(r'^[А-Яа-я]+$', city)

        if not match:
            raise serializers.ValidationError('Неверный формат')

        return city


class PersonGetPatchSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Person
        exclude = [
            'address',
            'domain',
            'user'
        ]


class PersonCityEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']
