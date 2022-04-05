import datetime

from rest_framework import serializers

from speakers.settings import DEFAULT_HOST
from workroomsapp.calendar.utils import build_photo_path
from workroomsapp.lecture.utils import (
    convert_datetime,
    check_datetime_for_lecture_as_lecturer
)
from workroomsapp.models import Lecture, CustomerLectureRequest, Person, LecturerLectureRequest


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


class LecturesGetSerializer(serializers.Serializer):
    lecture_id = serializers.SerializerMethodField()
    lecture_name = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    hall_address = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    creator_first_name = serializers.SerializerMethodField()
    creator_last_name = serializers.SerializerMethodField()
    in_respondents = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'lecture_id',
            'lecture_name',
            'dates',
            'hall_address',
            'description',
            'photo',
            'in_respondents',
            'creator_first_name',
            'creator_last_name',
        ]

    def get_lecture_id(self, obj):
        return obj.lecture_request.lecture.pk

    def get_lecture_name(self, obj):
        return obj.lecture_request.lecture.name

    def get_dates(self, obj):
        return obj.lecture_request.event.datetime_start

    def get_description(self, obj):
        return obj.lecture_request.lecture.description

    def get_in_respondents(self, obj):
        return bool(obj.lecture_request.respondents.filter(person=self.context['request'].user.person).first())

    def get_hall_address(self, obj):
        return obj.lecture_request.lecture.optional.hall_address

    def get_photo(self, obj):
        return DEFAULT_HOST + obj.photo.url

    def get_creator_first_name(self, obj):
        if hasattr(obj, 'customer'):
            return obj.customer.person.first_name
        return obj.lecturer.person.first_name

    def get_creator_last_name(self, obj):
        if hasattr(obj, 'customer'):
            return obj.customer.person.last_name
        return obj.lecturer.person.last_name
