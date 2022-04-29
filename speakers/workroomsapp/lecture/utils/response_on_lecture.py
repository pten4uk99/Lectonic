import datetime

from chatapp.models import Chat, Message
from workroomsapp.calendar.utils import get_model_from_attrs
from workroomsapp.lecture import lecture_responses
from workroomsapp.models import Lecture
from workroomsapp.utils.ws import WsMessageSender


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


class LectureToggleConfirmBaseMixin(LectureResponseBaseMixin):
    def get_params(self):
        params = super().get_params()

        respondent_id = self.request.GET.get('respondent')
        chat_id = self.request.GET.get('chat_id')

        if not (respondent_id and chat_id):
            return lecture_responses.not_in_data()

        params['respondent_id'] = respondent_id
        params['chat_id'] = chat_id

        return params

    def get_responses(self):
        """ Проверяет, является ли выбранный пользователь откликнувшимся на данную лекцию и
        возвращает объекты LectureRequest принадлежащие текущему чату """

        lecture_requests = self.get_lecture().lecture_requests.filter(chat_list=self.get_chat())

        if not lecture_requests:
            return lecture_responses.not_a_respondent()

        return lecture_requests

    def get_chat(self):
        """ Возвращает объект модели Chat """

        return Chat.objects.get(pk=self.get_params()['chat_id'])

    def handle_respondent(self):
        """ Базовый метод для обработки откликнувшегося пользователя """

        raise NotImplementedError()

    def check_is_creator(self):
        """ Проверяет, является ли пользователь создателем лекции """

        lecture = self.get_lecture()
        lecture_user = get_model_from_attrs(lecture, ['lecturer', 'customer']).person.user

        if not lecture_user == self.request.user:
            return lecture_responses.not_a_creator()

    def get_message_data(self):
        """ Возвращает данные для сообщения веб сокета """

        return {
            'type': 'chat_message',
            'chat_id': self.get_params()['chat_id'],
            'author': self.request.user.pk,
            'text': '',
            # в классах-наследниках должен быть добавлен ключ 'confirm' со значениями True/False
        }

    def create_message(self):
        data = self.get_message_data()
        Message.objects.create(
            author=self.request.user,
            chat=self.get_chat(),
            text=data['text'],
            confirm=data['confirm']
        )
        return data

    def handle_message(self):
        """ Создает сообщение о подтверждении/отклонении лекции (объект Message) и
        отправляет его по веб сокету """

        message_data = self.create_message()
        self.send_ws_message(clients=self.get_chat().users.all(), message=message_data)


class LectureConfirmRespondentMixin(LectureToggleConfirmBaseMixin):
    def handle_respondent(self):
        """ Подтверждает откликнувшегося пользователя на выбранные даты """

        for lecture_request in self.get_responses():
            lecture_respondent = lecture_request.respondent_obj.get(person=self.get_params()['respondent_id'])
            lecture_respondent.confirmed = True
            lecture_respondent.save()

    def get_message_data(self):
        data = super().get_message_data()
        data['confirm'] = True
        return data


class LectureRejectRespondentMixin(LectureToggleConfirmBaseMixin):
    def handle_respondent(self):
        """ Отклоняет откликнувшегося пользователя на выбранные даты """

        for lecture_request in self.get_responses():
            lecture_respondent = lecture_request.respondent_obj.get(person=self.get_params()['respondent_id'])
            lecture_respondent.rejected = True
            lecture_respondent.save()

    def get_message_data(self):
        data = super().get_message_data()
        data['confirm'] = False
        return data
