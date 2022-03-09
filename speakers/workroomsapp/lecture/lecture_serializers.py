from rest_framework import serializers

from workroomsapp.models import Lecture


class LectureCreateAsLecturerSerializer(serializers.Serializer):
    name = serializers.CharField()
    datetime = serializers.DateTimeField()
    hall_address = serializers.CharField()
    equipment = serializers.CharField()
    type = serializers.CharField()
    status = serializers.BooleanField()
    duration = serializers.IntegerField()
    cost = serializers.IntegerField()
    description = serializers.CharField()

    class Meta:
        fields = [
            'name',
            'hall_address',
            'equipment',
            'type',
            'status',
            'duration',
            'cost',
            'description',
        ]

    def create(self, validated_data):
        return Lecture.objects.create_as_lecturer(
            lecturer=self.context['request'].user.person.lecturer,
            name=validated_data.get('name'),
            datetime=validated_data.get('datetime'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            lecture_type=validated_data.get('type'),
            status=validated_data.get('status'),
            duration=validated_data.get('duration'),
            cost=validated_data.get('cost'),
            description=validated_data.get('description'),
        )
