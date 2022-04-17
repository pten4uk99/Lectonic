import datetime

from rest_framework import serializers

from speakers.settings import DEFAULT_HOST
from workroomsapp.lecture.utils import (
    convert_datetime,
    check_datetime_for_lecture_as_lecturer
)
from workroomsapp.models import Lecture, Person, Respondent


class LectureCreateAsLecturerSerializer(serializers.Serializer):
    name = serializers.CharField()
    svg = serializers.IntegerField(min_value=1)
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
            'svg',
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

    def validate_datetime(self, datetime_list):
        dates = []
        for elem in datetime_list:
            start, end = elem.split(',')
            start, end = convert_datetime(start, end)

            if not check_datetime_for_lecture_as_lecturer(
                    self.context['request'].user.person.lecturer, start.date(), start.time(), end.time()):
                raise serializers.ValidationError(f'Событие на выбранное время уже существует {start} - {end}')

            if start < datetime.datetime.now() + datetime.timedelta(hours=1):
                msg = 'Невозможно создать событие на прошедшую дату'
                raise serializers.ValidationError(msg)

            dates.append([start, end])

        return dates

    def create(self, validated_data):
        return Lecture.objects.create_as_lecturer(
            lecturer=self.context['request'].user.person.lecturer,
            name=validated_data.get('name'),
            svg=validated_data.get('svg'),
            domain=validated_data.get('domain'),
            datetime=validated_data.get('datetime'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            lecture_type=validated_data.get('type'),
            cost=validated_data.get('cost', 0),
            description=validated_data.get('description'),
        )


class LecturesGetSerializer(serializers.Serializer):
    lecture_id = serializers.SerializerMethodField()
    svg = serializers.SerializerMethodField()
    lecture_type = serializers.SerializerMethodField()
    lecture_name = serializers.SerializerMethodField()
    domain = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    hall_address = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    equipment = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    creator_is_lecturer = serializers.SerializerMethodField()
    creator_user_id = serializers.SerializerMethodField()
    creator_first_name = serializers.SerializerMethodField()
    creator_photo = serializers.SerializerMethodField()
    creator_last_name = serializers.SerializerMethodField()
    creator_middle_name = serializers.SerializerMethodField()
    can_response = serializers.SerializerMethodField()
    response_dates = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'lecture_id',
            'svg',
            'lecture_name',
            'lecture_type',
            'dates',
            'hall_address',
            'description',
            'can_response',
            'creator_user_id',
            'creator_first_name',
            'creator_last_name',
            'creator_middle_name',
        ]

    def get_lecture_id(self, obj):
        return obj.pk

    def get_svg(self, obj):
        return obj.svg

    def get_lecture_type(self, obj):
        return obj.get_type_display()

    def get_lecture_name(self, obj):
        return obj.name

    def get_domain(self, obj):
        return obj.lecture_domains.all().values_list('domain__name', flat=True)

    def get_dates(self, obj):
        dates = []
        lecture_requests = obj.lecture_requests.all()
        for lecture_request in lecture_requests:
            dates.append({
                'start': lecture_request.event.datetime_start,
                'end': lecture_request.event.datetime_end,
            })
        return dates

    def get_description(self, obj):
        return obj.description

    def get_equipment(self, obj):
        return obj.optional.equipment

    def get_cost(self, obj):
        return obj.cost

    def get_hall_address(self, obj):
        return obj.optional.hall_address

    def get_creator_is_lecturer(self, obj):
        return bool(obj.lecturer)

    def get_creator_first_name(self, obj):
        if obj.customer:
            return obj.customer.person.first_name
        return obj.lecturer.person.first_name

    def get_creator_user_id(self, obj):
        if obj.customer:
            return obj.customer.person.user.pk
        return obj.lecturer.person.user.pk

    def get_creator_photo(self, obj):
        if obj.customer:
            if obj.customer.person.photo:
                return DEFAULT_HOST + obj.customer.person.photo.url
            return ''
        if obj.lecturer.person.photo:
            return DEFAULT_HOST + obj.lecturer.person.photo.url
        return ''

    def get_creator_last_name(self, obj):
        if obj.customer:
            return obj.customer.person.last_name
        return obj.lecturer.person.last_name

    def get_creator_middle_name(self, obj):
        if obj.customer:
            return obj.customer.person.middle_name
        return obj.lecturer.person.middle_name

    def get_can_response(self, obj):
        person = self.context['request'].user.person
        for lecture_request in obj.lecture_requests.all():
            respondent = Respondent.objects.filter(person=person, lecture_request=lecture_request).first()
            if respondent and not (respondent.rejected or respondent.confirmed):
                return False
        return True

    def get_response_dates(self, obj):
        person = self.context['request'].user.person
        data = []

        for lecture_request in person.responses.filter(lecture=obj):
            respondent = Respondent.objects.get(person=person, lecture_request=lecture_request)
            data.append({
                'date': lecture_request.event.datetime_start,
                'rejected': respondent.rejected
            })

        return data
