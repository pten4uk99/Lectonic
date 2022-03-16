import datetime

from rest_framework import serializers

from workroomsapp.models import Lecture


class LectureCreateAsLecturerSerializer(serializers.Serializer):
    name = serializers.CharField()
    photo = serializers.FileField()
    domain = serializers.ListField()
    date = serializers.DateField()
    time_start = serializers.TimeField()
    time_end = serializers.TimeField()
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

    def validate(self, data):
        date = data.pop('date')
        time_start = data.pop('time_start')
        time_end = data.pop('time_end')

        data['datetime'] = datetime.datetime(date.year, date.month, date.day,
                                             time_start.hour, time_start.minute)
        data['duration'] = (datetime.timedelta(hours=time_end.hour, minutes=time_end.minute) -
                            datetime.timedelta(hours=time_start.hour, minutes=time_end.minute)).seconds // 60
        return data

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
            duration=validated_data.get('duration'),
            cost=validated_data.get('cost', 0),
            description=validated_data.get('description'),
        )
