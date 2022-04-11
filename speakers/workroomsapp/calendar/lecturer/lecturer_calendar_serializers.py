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
            Q(datetime_start__gte=datetime.datetime.now())
        )

        data = []

        for event in events:
            year = event.datetime_start.year
            month = event.datetime_start.month
            day = event.datetime_start.day

            lecture = event.lecture_request.lecture
            person = lecture.lecturer.person

            respondents = event.lecture_request.respondents.all()
            respondent_list = []
            for respondent in respondents:
                respondent_list.append({
                    'id': respondent.user.pk,
                    'first_name': respondent.first_name,
                    'last_name': respondent.last_name
                })

            new_event = {
                'creator': [person.first_name, person.last_name],
                'customer': '',
                'svg': lecture.svg,
                'respondents': respondent_list,
                'name': lecture.name,
                'hall_address': lecture.optional.hall_address,
                'status': lecture.status,
                'start': event.datetime_start.strftime('%H:%M'),
                'end': event.datetime_end.strftime('%H:%M')
            }

            if lecture.confirmed_person:
                confirmed_person = lecture.confirmed_person
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


class LecturerCalendarResponsesSerializer(serializers.Serializer):
    calendar = serializers.SerializerMethodField()

    class Meta:
        fields = ['calendar']

    def get_date_events(self, obj):
        request = self.context['request']
        year = request.GET.get('year')
        month = request.GET.get('month')

        if not (year and month):
            raise serializers.ValidationError({'detail': "В запросе не передана дата"})

        events = []
        lecture_requests = request.user.person.responses.order_by('event__datetime_start').filter(
            Q(event__datetime_start__year=year) &
            Q(event__datetime_start__month=month) &
            Q(event__datetime_start__gte=datetime.datetime.now())
        )

        for lecture_request in lecture_requests:
            if lecture_request.lecture.customer:
                events.append(lecture_request.event)

        data = []

        for event in events:
            year = event.datetime_start.year
            month = event.datetime_start.month
            day = event.datetime_start.day

            lecture = event.lecture_request.lecture
            creator = None
            if lecture.customer:
                creator = lecture.customer.person
            elif lecture.lecturer:
                creator = lecture.lecturer.person

            new_event = {
                'creator': [creator.first_name, creator.last_name],
                'lecturer': '',
                'svg': lecture.svg,
                'respondents': [],
                'name': lecture.name,
                'status': lecture.status,
                'hall_address': lecture.optional.hall_address,
                'start': event.datetime_start.strftime('%H:%M'),
                'end': event.datetime_end.strftime('%H:%M')
            }

            if lecture.confirmed_person:
                confirmed_person = lecture.confirmed_person
                new_event['lecturer'] = [confirmed_person.last_name,
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
