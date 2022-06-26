from typing import NamedTuple

from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from chatapp.models import Message, Chat
from chatapp.services.ws_message import WsMessage, WsEventTypes, WsMessageSender, WsMessageBuilder
from speakers.service import Service
from workroomsapp.lecture.services.db import ChatManager
from workroomsapp.models import LectureRequest, Person


class DeletedChat(NamedTuple):
    client: User
    chat_id: int


class WsService(Service):
    message_builder = WsMessageBuilder
    message_sender = WsMessageSender

    def __init__(self, request: HttpRequest, from_obj: User, clients: list[User]):
        super().__init__(from_obj)
        self.message_builder = self.message_builder(request)
        self.clients = clients

    def get_message(self) -> dict:
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

    def get_message(self):
        chat = self.chat_manager.get_chat_by_dates(
            self.responses,
            creator=self._lecture_creator.user,
            respondent=self.from_obj
        )
        return self.message_builder.new_respondent(chat)

    def setup(self) -> None:
        """ Создает сообщение для вебсокета и отправляет его """

        message = WsMessage(type_=WsEventTypes.new_respondent, kwargs=self.get_message())
        sender = self.message_sender(self.clients, message)
        sender.send()


class LectureCancelResponseWsService(WsService):
    def __init__(self, request: HttpRequest, from_obj: User, clients: list[User], chat_id: int):
        super().__init__(request, from_obj, clients=clients)
        self.chat_id = chat_id

    def get_message(self):
        return self.message_builder.remove_respondent(self.chat_id)

    def setup(self):
        message = WsMessage(type_=WsEventTypes.remove_respondent, kwargs=self.get_message())
        sender = self.message_sender(self.clients, message)
        sender.send()


class LectureConfirmRespondentWsService(WsService):
    chat_manager = ChatManager

    def __init__(self, request: HttpRequest, from_obj: User,
                 messages: list[Message], deleted_chats: list[DeletedChat]):
        super().__init__(request, from_obj, clients=[])
        self.messages = messages
        self.deleted_chats = deleted_chats

    def _get_client_from_chat(self, chat: Chat) -> User:
        return self.chat_manager.get_user_from_chat(chat, exclude_user=self.from_obj)

    def _make_message(self, message: Message) -> WsMessage:
        built_message = self.message_builder.chat_message(message)
        built_message['confirm'] = True

        return WsMessage(
            type_=WsEventTypes.chat_message, kwargs=built_message)

    def _send_message(self, message: Message) -> None:
        """ Создает и отправляет сообщение для откликнувшихся пользователей на подтвержденную дату """

        client = self._get_client_from_chat(message.chat)
        ws_message = self._make_message(message)
        sender = self.message_sender([client], ws_message)
        sender.send()

    def _make_deleted_chat_message(self, chat_id: int) -> WsMessage:
        return WsMessage(
            type_=WsEventTypes.read_reject_chat, kwargs=self.message_builder.read_reject_chat(chat_id))

    def _send_deleted_chat_message(self, deleted_chat: DeletedChat) -> None:
        """ Создает и отправляет сообщение для чата, который был удален """

        client, chat_id = deleted_chat
        ws_message = self._make_deleted_chat_message(chat_id)
        sender = self.message_sender([client], ws_message)
        sender.send()

    def _send_messages(self) -> None:
        """ Отправляет сообщения self.messages и self.deleted_chats """

        for message in self.messages:
            self._send_message(message)

        for deleted_chat in self.deleted_chats:
            self._send_deleted_chat_message(deleted_chat)

    def setup(self):
        self._send_messages()
