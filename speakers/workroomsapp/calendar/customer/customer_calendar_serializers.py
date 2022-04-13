import datetime

from django.db.models import Q
from rest_framework import serializers

from speakers.settings import DEFAULT_HOST
from workroomsapp.calendar.utils import CalendarDataSerializer
from workroomsapp.models import CustomerCalendar


class CustomerCalendarSerializer(serializers.ModelSerializer):
    calendar = serializers.SerializerMethodField()

    class Meta:
        model = CustomerCalendar
        fields = ['calendar']

    def get_calendar(self, obj):
        return CalendarDataSerializer(serializer_obj=self,
                                      owner_attr='customer',
                                      opponent_attr='lecturer'
                                      ).build_events_serialize()


class CustomerCalendarResponsesSerializer(serializers.Serializer):
    calendar = serializers.SerializerMethodField()

    class Meta:
        fields = ['calendar']

    def get_calendar(self, obj):
        return CalendarDataSerializer(
            serializer_obj=self,
            owner_attr='lecturer',
            opponent_attr='customer',
            responses=True
        ).build_events_serialize()
