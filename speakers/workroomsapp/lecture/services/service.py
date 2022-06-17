import datetime
import logging

from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from chatapp.models import Chat
from chatapp.services.ws import WsMessage, WsEventTypes, WsMessageBuilder, WsMessageSender
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.services.db import DeleteLectureManager, AttrNames, LectureResponseManager, ChatManager
from workroomsapp.models import Lecture, LectureRequest, Person

logger = logging.getLogger(__name__)


class Service:
    """ Реализует бизнес логику проекта """

    object_manager = None

    def __init__(self, from_obj: User, from_attr: AttrNames = AttrNames.LECTURER):
        self._from_attr = from_attr
        self._from_obj = from_obj

        if self.object_manager is not None:
            self.object_manager = self.object_manager(from_attr)


class WsService(Service):
    chat_manager = ChatManager
    message_builder = WsMessageBuilder
    message_sender = WsMessageSender

    def __init__(self, request: HttpRequest, from_obj: User,
                 clients: list[User], responses: QuerySet[LectureRequest],
                 lecture_creator: Person, from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj, from_attr)
        self.request = request
        self.chat_manager = self.chat_manager()
        self.message_builder = self.message_builder(request)
        self.clients = clients
        self.responses = responses
        self._lecture_creator = lecture_creator

    @property
    def clients(self):
        return self._clients

    @clients.setter
    def clients(self, value):
        if not isinstance(value, list):
            raise TypeError("Значение аттрибута clients должно быть списком")
        for client in value:
            if not isinstance(client, User):
                raise TypeError("Получатель должен быть класса User")

        self._clients = value

    def _get_message(self) -> dict:
        chat = self.chat_manager.get_chat_by_dates(
            self.responses,
            creator=self._lecture_creator.user,
            respondent=self._from_obj.person
        )
        return self.message_builder.new_respondent(chat)

    def new_response(self) -> None:
        """ Создает сообщение для вебсокета и отправляет его """

        message = WsMessage(type_=WsEventTypes.new_respondent, kwargs=self._get_message())
        sender = self.message_sender(self.clients, message)
        sender.send()


class ChatService(Service):
    response_message_text = 'Собеседник заинтересован в Вашем предложении. ' \
                            'Возможные даты проведения:'
    object_manager = ChatManager

    def __init__(self, from_obj: User, lecture: Lecture,
                 responses: QuerySet[LectureRequest], lecture_creator: Person,
                 from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj, from_attr)
        self._lecture = lecture
        self._lecture_responses = responses
        self._lecture_creator = lecture_creator

    def _format_dates_for_message(self) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        dates = []

        for response in self._lecture_responses:
            dates.append(response.event.datetime_start.strftime('%d.%m'))

        return dates

    def _make_response_message_text(self) -> str:
        """ Объединяет сообщение self.response_message_text и отформатированные даты лекции """

        dates = self._format_dates_for_message()
        str_dates = ", ".join(dates)
        return self.response_message_text + ' ' + str_dates

    def _create_chat(self) -> Chat:
        """ Возвращает объект Chat по переданным датам """

        responses = self._lecture_responses
        chat = self.object_manager.get_chat_by_dates(
            dates=responses, creator=self._lecture_creator.user, respondent=self._from_obj)

        if not chat:
            chat = self.object_manager.create_chat(self._lecture)
            self.object_manager.add_responses(chat, responses, save=False)
            self.object_manager.add_users(
                chat, creator=self._lecture_creator.user, respondent=self._from_obj, save=False)
            chat.save()

        # logger.info(f'chat: {chat}')
        return chat

    def _create_response_message(self) -> None:
        """ Создает в чате стандартное сообщение при отклике """

        message = self.object_manager.create_message(
            self._create_chat(), self._from_obj, self._make_response_message_text())

        # logger.info(f'text:{message.text}, author: {message.author}')

    def new_response(self) -> None:
        """ Создает новый чат (если его до этого не существовало) и
        стандартное сообщение в чате при отклике """

        self._create_chat()
        self._create_response_message()


class LectureService(Service):
    def _check_permissions(self, *args, **kwargs) -> bool:
        """ Проверяет права """

        return True

    def to_do(self, *args, **kwargs) -> None:
        """ Метод, который вызывается снаружи класса, чтобы он выполнил свою работу """

        self._check_permissions()


class LectureDeleteService(LectureService):
    object_manager = DeleteLectureManager

    def __init__(self, from_obj: User, lecture_id: int):
        super().__init__(from_obj=from_obj)
        self._lecture = self.object_manager.get_lecture_by_id(int(lecture_id))

    def _check_permissions(self) -> bool:
        """ Проверяет является ли пользователь (self._from_obj), создателем лекции (lecture) """

        if self._lecture.lecturer:
            if not self._lecture.lecturer.person.user == self._from_obj:
                return lecture_responses.not_a_creator()
        elif self._lecture.customer:
            if not self._lecture.customer.person.user == self._from_obj:
                return lecture_responses.not_a_creator()

        return True

    def to_do(self) -> None:
        """ Удаляет объект Lecture из базы данных """

        super().to_do()
        self.object_manager.delete(self._lecture)


class LectureResponseService(LectureService):
    object_manager = LectureResponseManager
    chat_service = ChatService
    ws_service = WsService

    def __init__(self, request: HttpRequest, from_obj: User,
                 lecture: Lecture, response_dates: list[str],
                 from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj, from_attr=from_attr)
        self._lecture = lecture
        self._lecture_creator = self._get_lecture_creator()
        self._responses = self._get_lecture_dates(response_dates)
        self._chat_service = self.chat_service(
            from_obj=from_obj, lecture=lecture,
            responses=self._responses, lecture_creator=self._lecture_creator)
        self._ws_service = self.ws_service(
            request, from_obj=from_obj, clients=[self._lecture_creator.user, self._from_obj],
            lecture_creator=self._lecture_creator, responses=self._responses)

    def _get_lecture_creator(self) -> Person:
        """ Возвращает объект Person создателя лекции. """

        creator = None

        if not self._lecture.customer:
            if not hasattr(self._from_obj.person, 'customer'):
                return lecture_responses.lecturer_forbidden()
        else:
            creator = self._lecture.customer.person

        if not self._lecture.lecturer:
            if not hasattr(self._from_obj.person, 'lecturer'):
                return lecture_responses.customer_forbidden()
        else:
            creator = self._lecture.lecturer.person

        return creator

    def _check_can_response(self):
        """ Проверяет, может ли пользователь откликнуться на текущую лекцию """

        lecture_requests = self.object_manager.get_person_rejected_lecture_requests(
            self._from_obj.person, self._lecture)
        if lecture_requests:
            return lecture_responses.can_not_response()

    def _check_permissions(self, *args, **kwargs) -> bool:
        self._check_can_response()
        return super()._check_permissions()

    # возможно форматирование дат стоит перенести куда-нибудь отдельно
    @staticmethod
    def _format_dates(dates: list[str]) -> list[datetime.datetime]:
        """ Форматирует переданные в запросе даты """

        format_dates = []

        for date in dates:
            format_dates.append(
                datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M'))

        return format_dates

    def _get_lecture_dates(self, dates: list[str]) -> QuerySet[LectureRequest]:
        """ Возвращает список LectureRequests по датам лекции """

        response_dates = self._format_dates(dates)
        return self.object_manager.get_responses(self._lecture, response_dates)

    def _add_respondent(self) -> None:
        """ Добавляет пользователя в откликнувшиеся на переданные даты лекции """

        self.object_manager.add_respondent(self._from_obj.person, self._responses)
        logger.info(f'responses: {self._responses}')

    def to_do(self):
        super().to_do()  # проверяется возможность отклика
        self._add_respondent()  # пользователь добавляется в откликнувшиеся

        # сообщает дополнительным сервисам о новом отклике
        self._chat_service.new_response()
        self._ws_service.new_response()
