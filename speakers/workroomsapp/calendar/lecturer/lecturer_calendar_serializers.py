import datetime

from django.db.models import Q
from rest_framework import serializers

from speakers.settings import DEFAULT_HOST
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

        events = obj.calendar.events.order_by('datetime_start').filter(
            Q(datetime_start__year=year) &
            Q(datetime_start__month=month) &
            Q(datetime_start__day__gte=datetime.datetime.now().day)
        )

        data = []

        for event in events:
            year = event.datetime_start.year
            month = event.datetime_start.month
            day = event.datetime_start.day

            person = event.lecture_request.lecturer_lecture_request.lecturer.person
            lecture = event.lecture_request.lecture

            respondents = event.lecture_request.respondents.all()
            confirmed_respondent = respondents.filter(confirmed=True).first()
            respondent_list = []
            for respondent in respondents:
                respondent_list.append({
                    'id': respondent.person.user.pk,
                    'first_name': respondent.person.first_name,
                    'last_name': respondent.person.last_name
                })

            new_event = {
                'creator': [person.first_name, person.last_name],
                'customer': '',
                'photo': DEFAULT_HOST + event.lecture_request.lecturer_lecture_request.photo.url,
                'respondents': respondent_list,
                'name': lecture.name,
                'hall_address': lecture.optional.hall_address,
                'status': lecture.status,
                'start': event.datetime_start.strftime('%H:%M'),
                'end': event.datetime_end.strftime('%H:%M')
            }

            if confirmed_respondent:
                confirmed_person = confirmed_respondent.person
                new_event['customer'] = [confirmed_person.last_name,
                                         confirmed_person.first_name,
                                         confirmed_person.middle_name or ""]

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
