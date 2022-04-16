import datetime

from django.db.models import Q

from workroomsapp.models import Respondent


def build_photo_path(request, part_of_path):
    host = request.build_absolute_uri('/')

    if host[-1] == '/' and part_of_path[0] == '/':
        new_path = part_of_path.replace('/', '', 1)
        return host + new_path

    elif host[-1] != '/' and part_of_path[0] != '/':
        return host + '/' + part_of_path

    return host + part_of_path


def get_model_from_attrs(model, attr_names=None):
    if attr_names is None:
        attr_names = []

    list_of_attrs = []

    for attr in attr_names:
        if hasattr(model, attr):
            list_of_attrs.append(getattr(model, attr))

    if not list_of_attrs:
        return False
    if len(list_of_attrs) == 1:
        return list_of_attrs[0]
    return list_of_attrs


class CalendarDataGripper:
    def __init__(self, serializer_obj, owner_attr: str):
        self.request = serializer_obj.context['request']
        self.model = serializer_obj.instance
        self.owner_attr = owner_attr

    def get_events(self):
        return self.model.calendar.events.order_by(
            'datetime_start').select_related(
            'lecture_request').prefetch_related(
            'lecture_request__respondents').filter(
            Q(datetime_start__gte=datetime.datetime.now())
        )

    def get_responses_events(self):
        events = []
        lecture_requests = self.request.user.person.responses.order_by(
            'event__datetime_start').filter(
            event__datetime_start__gte=datetime.datetime.now(),
            respondent__rejected=False
        )

        for lecture_request in lecture_requests:
            lecture = lecture_request.lecture

            if get_model_from_attrs(lecture, [self.owner_attr]):
                events.append(lecture_request.event)

        return events

    @staticmethod
    def get_lecture(event):
        return event.lecture_request.lecture

    def get_person(self, event):
        lecture = self.get_lecture(event)
        return get_model_from_attrs(lecture, [self.owner_attr]).person

    def get_lecture_creator(self, event):
        return get_model_from_attrs(self.get_lecture(event), [self.owner_attr]).person

    @staticmethod
    def get_respondents(event):
        return event.lecture_request.respondents.all()

    @staticmethod
    def get_respondent_confirmed(person, lecture_request):
        return Respondent.objects.get(person=person, lecture_request=lecture_request).confirmed


class CalendarDataSerializer:
    def __init__(self, serializer_obj, owner_attr, opponent_attr, responses: bool = False):
        self.data_gripper = CalendarDataGripper(serializer_obj, owner_attr)
        self.responses = responses
        self.opponent_attr = opponent_attr

    def get_respondent_list_serialize(self, event):
        respondent_list = []
        confirmed_respondent = False

        for respondent in self.data_gripper.get_respondents(event):
            confirmed = self.data_gripper.get_respondent_confirmed(
                respondent, event.lecture_request)

            if confirmed:
                confirmed_respondent = respondent

            respondent_list.append({
                'id': respondent.user.pk,
                'first_name': respondent.first_name,
                'last_name': respondent.last_name,
                'middle_name': respondent.middle_name or "",
                'confirmed': confirmed,
            })

        return respondent_list, confirmed_respondent

    def get_event_serialize(self, event):
        if self.responses:
            creator = self.data_gripper.get_lecture_creator(event)
        else:
            creator = self.data_gripper.get_person(event)

        lecture = self.data_gripper.get_lecture(event)

        respondent_list, confirmed_respondent = self.get_respondent_list_serialize(event)

        data = {
            'creator': [creator.first_name, creator.last_name],
            'svg': lecture.svg,
            'respondents': respondent_list,
            'name': lecture.name,
            'hall_address': lecture.optional.hall_address,
            'start': event.datetime_start.strftime('%H:%M'),
            'end': event.datetime_end.strftime('%H:%M')
        }

        if confirmed_respondent:
            data['status'] = True

            if self.responses:
                data[self.data_gripper.owner_attr] = [creator.last_name,
                                                      creator.first_name,
                                                      creator.middle_name or ""]
            else:
                data[self.opponent_attr] = [confirmed_respondent.last_name,
                                            confirmed_respondent.first_name,
                                            confirmed_respondent.middle_name or ""]

        return data

    def build_events_serialize(self):
        if self.responses:
            event_list = self.data_gripper.get_responses_events()
        else:
            event_list = self.data_gripper.get_events()

        data = []

        for event in event_list:
            year = event.datetime_start.year
            month = event.datetime_start.month
            day = event.datetime_start.day

            new_event = self.get_event_serialize(event)

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
