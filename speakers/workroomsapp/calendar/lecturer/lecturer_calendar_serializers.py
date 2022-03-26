import datetime

from django.db.models import Q
from rest_framework import serializers

from workroomsapp.calendar.utils import build_photo_path
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
        request = self.context['request']
        year = request.GET.get('year')
        month = request.GET.get('month')

        if not (year and month):
            raise serializers.ValidationError({'detail': "В запросе не передана дата"})

        events = obj.calendar.events.order_by('datetime').filter(
            Q(datetime__year=year) & Q(datetime__month=month))

        data = []

        for event in events:
            year = event.datetime.year
            month = event.datetime.month
            day = event.datetime.day

            person = event.lecture_request.lecturer_lecture_request.lecturer.person
            lecture = event.lecture_request.lecture

            time_end = event.datetime + datetime.timedelta(minutes=lecture.duration)
            new_event = {
                'lecturer': f'{person.last_name} {person.first_name} {person.middle_name or ""}',
                'photo': build_photo_path(request, event.lecture_request.lecturer_lecture_request.photo.url),
                'name': lecture.name,
                'status': lecture.status,
                'start': event.datetime.strftime('%H:%M'),
                'end': time_end.strftime('%H:%M')
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
