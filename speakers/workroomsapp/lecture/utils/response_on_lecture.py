import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from chatapp.models import WsClient
from workroomsapp.lecture import lecture_responses
from workroomsapp.models import Lecture


class WsMessageSender:
    channel_layer = get_channel_layer()

    def __init__(self, clients: list, message: dict):
        self.message = message
        self.clients = WsClient.objects.filter(user__in=clients)

    def send(self):
        for client in self.clients:
            async_to_sync(self.channel_layer.send)(getattr(client, 'channel_name', ''), self.message)


class LectureResponseBaseMixin:
    def get_params(self):
        """ Получает параметр лекции из запроса и проверяет передан он или нет. """

        lecture_id = self.request.GET.get('lecture')

        if not lecture_id:
            return lecture_responses.not_in_data()

        return {'lecture_id': lecture_id}

    def get_lecture(self):
        """ Получает объект лекции """

        lecture = Lecture.objects.filter(pk=self.get_params()['lecture_id']).first()

        if not lecture:
            return lecture_responses.lecture_does_not_exist()

        return lecture

    def check_can_response(self):
        """ Базовый метод для проверки, может ли пользователь откликаться на текущую лекцию или нет """
        raise NotImplementedError('This method was not defined')

    def send_ws_message(self, clients, message):
        return WsMessageSender(clients=clients, message=message).send()


class LectureResponseMixin(LectureResponseBaseMixin):
    def get_params(self):
        """ Проверяет есть ли даты лекции в параметрах запроса и возвращает эти даты. """

        params = super().get_params()
        dates = self.request.GET.getlist('date')

        if not dates:
            return lecture_responses.not_in_data()

        params['dates'] = dates

        return params

    def get_creator(self):
        """ Получает и возвращает объект Person создателя лекции. """

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

    def check_can_response(self):
        """ Проверяет, может ли пользователь откликнуться на текущую лекцию """

        requests = self.get_lecture().lecture_requests.filter(
                    respondents=self.request.user.person, respondent_obj__rejected=True)
        if requests:
            return lecture_responses.can_not_response()

    def get_format_dates(self):
        """ Форматирует переданные в запросе даты. """

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


class LectureCancelResponseMixin(LectureResponseBaseMixin):
    def check_can_response(self):
        requests = self.get_lecture().lecture_requests.filter(
                    respondents=self.request.user.person, respondent_obj__rejected=True)
        if not requests:
            return lecture_responses.can_not_cancel_response()
