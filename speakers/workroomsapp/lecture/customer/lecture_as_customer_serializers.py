import datetime

from rest_framework import serializers


from workroomsapp.lecture.utils import (
    convert_datetime,
    check_datetime_for_lecture_as_customer,
)
from workroomsapp.models import Lecture, Lecturer


class LectureCreateAsCustomerSerializer(serializers.Serializer):
    name = serializers.CharField()
    svg = serializers.IntegerField(min_value=1)
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

            if not check_datetime_for_lecture_as_customer(
                    self.context['request'].user.person.customer, start.date(), start.time(), end.time()):
                raise serializers.ValidationError(f'Событие на выбранное время уже существует {start} - {end}')

            if start < datetime.datetime.now() + datetime.timedelta(hours=1):
                msg = 'Невозможно создать событие на прошедшую дату'
                raise serializers.ValidationError(msg)

            dates.append([start, end])

        return dates

    def create(self, validated_data):
        return Lecture.objects.create_as_customer(
            customer=self.context['request'].user.person.customer,
            name=validated_data.get('name'),
            svg=validated_data.get('svg'),
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
