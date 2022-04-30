import datetime

from rest_framework import serializers

from speakers.settings import DEFAULT_HOST
from workroomsapp.calendar.utils import get_model_from_attrs
from workroomsapp.lecture.utils.datetime import (
    convert_datetime,
    check_datetime_for_lecture_as_lecturer
)
from workroomsapp.models import Lecture, Respondent


class LectureCreateAsLecturerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
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


class LecturesGetSerializer(serializers.ModelSerializer):
    lecture_type = serializers.SerializerMethodField()
    domain = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    hall_address = serializers.StringRelatedField(source='optional.hall_address')
    equipment = serializers.StringRelatedField(source='optional.equipment')
    creator_is_lecturer = serializers.SerializerMethodField()
    creator_user_id = serializers.SerializerMethodField()
    creator_id = serializers.SerializerMethodField()
    creator_first_name = serializers.SerializerMethodField()
    creator_photo = serializers.SerializerMethodField()
    creator_last_name = serializers.SerializerMethodField()
    creator_middle_name = serializers.SerializerMethodField()
    creator_bgc_number = serializers.SerializerMethodField()
    can_response = serializers.SerializerMethodField()
    response_dates = serializers.SerializerMethodField()
    related_person = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = [
            'id',
            'svg',
            'name',
            'lecture_type',
            'dates',
            'domain',
            'hall_address',
            'listeners',
            'description',
            'equipment',
            'cost',
            'can_response',
            'response_dates',
            'related_person',
            'creator_user_id',
            'creator_is_lecturer',
            'creator_id',
            'creator_photo',
            'creator_first_name',
            'creator_last_name',
            'creator_middle_name',
            'creator_bgc_number'
        ]

    def get_lecture_type(self, obj):
        return obj.get_type_display()

    def get_domain(self, obj):
        return obj.lecture_domains.all().values_list('domain__name', flat=True)

    def get_dates(self, obj):
        dates = []
        lecture_requests = obj.lecture_requests.order_by('event__datetime_start').all()
        for lecture_request in lecture_requests:
            dates.append({
                'start': lecture_request.event.datetime_start,
                'end': lecture_request.event.datetime_end,
            })
        return dates

    def get_creator_is_lecturer(self, obj):
        return bool(obj.lecturer)

    def get_related_person(self, obj):
        query_from = self.context.get('query_from')

        if not query_from:
            return

        person = None

        if get_model_from_attrs(obj, [query_from]):  # проверяем является ли запрашивающий создателем лекции
            lecture_request = obj.lecture_requests.filter(respondent_obj__confirmed=True).first()
            person = lecture_request.respondent_obj.get(confirmed=True).person
        else:
            if obj.lecturer:
                person = obj.lecturer.person
            else:
                person = obj.customer.person

        return {
            'user_id': person.user.pk,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'middle_name': person.middle_name
        }

    def get_creator_id(self, obj):
        if obj.lecturer:
            return obj.lecturer.pk
        else:
            return obj.customer.pk

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

    def get_creator_bgc_number(self, obj):
        if obj.customer:
            return obj.customer.person.bgc_number
        return obj.lecturer.person.bgc_number

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
                'rejected': respondent.rejected,
                'confirmed': respondent.confirmed
            })

        return data
