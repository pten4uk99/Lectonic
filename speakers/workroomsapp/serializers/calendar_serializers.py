import datetime

from django.db.models import Q
from rest_framework import serializers

from workroomsapp.models import LecturerCalendar


class LecturerCalendarCurrentMonthSerializer(serializers.ModelSerializer):
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

            new_event = {
                'lecturers': event.lecture.lecturers.all().values(
                    'person__first_name',
                    'person__last_name',
                    'person__middle_name'
                ),
                'name': event.lecture.name,
                'status': event.lecture.status,
            }

            if not data:
                data.append(
                    {
                        'date': datetime.datetime(year, month, day),
                        'events': [new_event]
                    }
                )

            found = False
            for date in data:
                if date.get('date') == datetime.datetime(year, month, day):
                    date['events'].append(new_event)
                    found = True

            if not found:
                data.append(
                    {
                        'date': datetime.datetime(year, month, day),
                        'events': [new_event]
                    }
                )

            print(data)
        return data

    def get_calendar(self, obj):
        return self.get_date_events(obj)
