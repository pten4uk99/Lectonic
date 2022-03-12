import datetime

from django.db.models import Q
from rest_framework import serializers

from workroomsapp.models import LecturerCalendar


class LecturerCalendarSerializer(serializers.ModelSerializer):
    lecturer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    calendar = serializers.SerializerMethodField()

    class Meta:
        model = LecturerCalendar
        fields = [
            'lecturer',
            'calendar'
        ]

    def get_date_events(self, obj):
        year = self.context['request'].GET.get('year')
        month = self.context['request'].GET.get('month')

        if not (year and month):
            raise serializers.ValidationError({'detail': "В запросе не передана дата"})

        events = obj.calendar.events.filter(
            Q(datetime__year=year) & Q(datetime__month=month))

        data = []

        for event in events:
            year = event.datetime.year
            month = event.datetime.month
            day = event.datetime.day

            person = event.lecture_request.lecturer_lecture_request.lecturer.person
            lecture = event.lecture_request.lecture

            new_event = {
                'lecturer': f'{person.last_name} {person.first_name}{ person.middle_name or ""}',
                'name': lecture.name,
                'status': lecture.status,
            }

            if not data:
                data.append(
                    {
                        'date': str(datetime.datetime(year, month, day)),
                        'events': [new_event]
                    }
                )

            found = False
            for date in data:
                if date.get('date') == str(datetime.datetime(year, month, day)):
                    if new_event not in date['events']:
                        date['events'].append(new_event)
                    found = True

            if not found:
                data.append(
                    {
                        'date': str(datetime.datetime(year, month, day)),
                        'events': [new_event]
                    }
                )
        return data

    def get_calendar(self, obj):
        return self.get_date_events(obj)
