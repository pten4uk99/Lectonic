import datetime

from rest_framework import serializers

from workroomsapp.lecture.utils import (
    convert_datetime,
    check_datetime_for_lecture_as_customer,
    check_datetime_for_lecture_as_lecturer
)
from workroomsapp.models import Lecture


class LectureCreateAsLecturerSerializer(serializers.Serializer):
    name = serializers.CharField()
    photo = serializers.FileField()
    domain = serializers.ListField()
    datetime = serializers.ListField()
    hall_address = serializers.CharField(required=False)
    equipment = serializers.CharField(required=False)
    type = serializers.CharField()
    cost = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        fields = [
            'name',
            'photo',
            'domain',
            'hall_address',
            'equipment',
            'type',
            'cost',
            'description',
        ]

    def validate_lecture(self, lecture):
        image_format = lecture.name.split('.')[-1]
        lecture.name = 'lecture.' + image_format
        return lecture

    def validate_photo(self, photo):
        image_format = photo.name.split('.')[-1]
        photo.name = 'photo.' + image_format
        return photo

    def validate_datetime(self, datetime_list):
        dates = []
        for elem in datetime_list:
            start, end = elem.split(',')
            start, end = convert_datetime(start, end)

            if not check_datetime_for_lecture_as_lecturer(
                    self.context['request'].user.person.lecturer, start.date(), start.time(), end.time()):
                raise serializers.ValidationError(f'Событие на выбранное время уже существует {start} - {end}')

            if start < datetime.datetime.now() + datetime.timedelta(days=1):
                msg = 'Между созданием и проведением лекции должно быть не менее 24 часов'
                raise serializers.ValidationError(msg)

            dates.append([start, end])

        return dates

    def create(self, validated_data):
        return Lecture.objects.create_as_lecturer(
            lecturer=self.context['request'].user.person.lecturer,
            name=validated_data.get('name'),
            photo=validated_data.get('photo'),
            domain=validated_data.get('domain'),
            datetime=validated_data.get('datetime'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            lecture_type=validated_data.get('type'),
            status=False,
            cost=validated_data.get('cost', 0),
            description=validated_data.get('description'),
        )


class LectureCreateAsCustomerSerializer(serializers.Serializer):
    name = serializers.CharField()
    photo = serializers.FileField()
    domain = serializers.ListField()
    datetime = serializers.ListField()
    hall_address = serializers.CharField(required=False)
    equipment = serializers.CharField(required=False)
    listeners = serializers.IntegerField()
    type = serializers.CharField()
    cost = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        fields = [
            'name',
            'photo',
            'domain',
            'hall_address',
            'equipment',
            'type',
            'cost',
            'description',
        ]

    def validate_lecture(self, lecture):
        image_format = lecture.name.split('.')[-1]
        lecture.name = 'lecture.' + image_format
        return lecture

    def validate_photo(self, photo):
        image_format = photo.name.split('.')[-1]
        photo.name = 'photo.' + image_format
        return photo

    def validate_datetime(self, datetime_list):
        dates = []
        for elem in datetime_list:
            start, end = elem.split(',')
            start, end = convert_datetime(start, end)

            if not check_datetime_for_lecture_as_customer(
                    self.context['request'].user.person.customer, start.date(), start.time(), end.time()):
                raise serializers.ValidationError(f'Событие на выбранное время уже существует {start} - {end}')

            if start < datetime.datetime.now() + datetime.timedelta(days=1):
                msg = 'Между созданием и проведением лекции должно быть не менее 24 часов'
                raise serializers.ValidationError(msg)

            dates.append([start, end])

        return dates

    def create(self, validated_data):
        return Lecture.objects.create_as_customer(
            customer=self.context['request'].user.person.customer,
            name=validated_data.get('name'),
            photo=validated_data.get('photo'),
            domain=validated_data.get('domain'),
            datetime=validated_data.get('datetime'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            listeners=validated_data.get('listeners'),
            lecture_type=validated_data.get('type'),
            status=False,
            cost=validated_data.get('cost', 0),
            description=validated_data.get('description'),
        )
