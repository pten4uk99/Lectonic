import datetime

from workroomsapp.lecture import lecture_responses
from workroomsapp.models import Lecture


class LectureResponseMixin:
    def get_params(self):
        lecture_id = self.request.GET.get('lecture')
        dates = self.request.GET.getlist('date')

        if not lecture_id or not dates:
            return lecture_responses.not_in_data()

        return {'lecture_id': lecture_id, 'dates': dates}

    def get_lecture(self):
        lecture = Lecture.objects.filter(pk=self.get_params()['lecture_id']).first()

        if not lecture:
            return lecture_responses.lecture_does_not_exist()

        return lecture

    def get_creator(self):
        lecture = self.get_lecture()
        creator = None

        if not lecture.customer:
            if not hasattr(self.request.user.person, 'customer'):
                return lecture_responses.lecturer_forbidden()
        else:
            creator = lecture.customer.person

        if not lecture.lecturer:
            if not hasattr(self.request.user.person, 'lecturer'):
                return lecture_responses.customer_forbidden()
        else:
            creator = lecture.lecturer.person
        return creator

    def check_can_response(self, cancel):
        requests = self.get_lecture().lecture_requests.filter(
                    respondents=self.request.user.person, respondent__rejected=True)
        if not cancel and requests:
            return lecture_responses.can_not_response()
        elif cancel and not requests:
            return lecture_responses.can_not_cancel_response()

    def get_format_dates(self):
        format_dates = []

        for date in self.get_params()['dates']:
            format_dates.append(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M'))

        return format_dates

    def get_responses(self):
        responses = self.get_lecture().lecture_requests.filter(
            event__datetime_start__in=self.get_format_dates())

        if not responses:
            return lecture_responses.does_not_exist()
        return responses
