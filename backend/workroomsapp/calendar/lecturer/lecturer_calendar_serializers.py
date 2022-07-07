import datetime

from django.db.models import Q
from rest_framework import serializers

from config.settings import DEFAULT_HOST
from workroomsapp.calendar.utils import build_photo_path, CalendarDataSerializer
from workroomsapp.models import LecturerCalendar


class LecturerCalendarSerializer(serializers.ModelSerializer):
    calendar = serializers.SerializerMethodField()

    class Meta:
        model = LecturerCalendar
        fields = ['calendar']

    def get_calendar(self, obj):
        return CalendarDataSerializer(
            serializer_obj=self,
            owner_attr='lecturer',
            opponent_attr='customer'
        ).build_events_serialize()


class LecturerCalendarResponsesSerializer(serializers.Serializer):
    calendar = serializers.SerializerMethodField()

    class Meta:
        fields = ['calendar']

    def get_calendar(self, obj):
        return CalendarDataSerializer(
            serializer_obj=self,
            owner_attr='customer',
            opponent_attr='lecturer',
            responses=True
        ).build_events_serialize()
