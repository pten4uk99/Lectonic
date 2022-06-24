from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from chatapp.services.ws_message import WsMessage, WsEventTypes, WsMessageSender, WsMessageBuilder
from speakers.service import Service
from workroomsapp.lecture.services.db import ChatManager
from workroomsapp.models import LectureRequest, Person


class WsService(Service):
    message_builder = WsMessageBuilder
    message_sender = WsMessageSender

    def __init__(self, request: HttpRequest, from_obj: User, clients: list[User]):
        super().__init__(from_obj)
        self.message_builder = self.message_builder(request)
        self.clients = clients

    def _get_message(self) -> dict:
        """ Возвращает сообщение для вебсокета """
        pass

    def setup(self) -> None:
        """ Собирает и запускает последовательно необходимые действия класса """
        pass


class LectureResponseWsService(WsService):
    chat_manager = ChatManager
    message_sender = WsMessageSender

    def __init__(self, request: HttpRequest, from_obj: User,
                 clients: list[User], responses: QuerySet[LectureRequest],
                 lecture_creator: Person):
        super().__init__(request, from_obj, clients=clients)
        self.request = request
        self.chat_manager = self.chat_manager()
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
                raise TypeError("Получатель должен быть типа User")

        self._clients = value

    def _get_message(self):
        chat = self.chat_manager.get_chat_by_dates(
            self.responses,
            creator=self._lecture_creator.user,
            respondent=self.from_obj
        )
        return self.message_builder.new_respondent(chat)

    def setup(self) -> None:
        """ Создает сообщение для вебсокета и отправляет его """

        message = WsMessage(type_=WsEventTypes.new_respondent, kwargs=self._get_message())
        sender = self.message_sender(self.clients, message)
        sender.send()


class LectureCancelResponseWsService(WsService):
    def __init__(self, request: HttpRequest, from_obj: User, clients: list[User], chat_id: int):
        super().__init__(request, from_obj, clients=clients)
        self.chat_id = chat_id

    def _get_message(self):
        return self.message_builder.remove_respondent(self.chat_id)

    def setup(self):
        message = WsMessage(type_=WsEventTypes.remove_respondent, kwargs=self._get_message())
        sender = self.message_sender(self.clients, message)
        sender.send()
