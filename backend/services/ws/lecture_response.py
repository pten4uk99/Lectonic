from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from chatapp.models import Message, Chat
from services.types import WsEventTypes
from services.ws.ws_message import WsMessageSender, WsMessage
from services.ws.base import WsService
from services.db.lecture import ChatManager
from workroomsapp.models import LectureRequest, Person


class LectureResponseWsService(WsService):
    chat_manager = ChatManager
    message_sender = WsMessageSender

    def __init__(self, from_obj: User,
                 clients: list[User], responses: QuerySet[LectureRequest],
                 lecture_creator: Person, ws_active: bool = True):
        super().__init__(from_obj, clients=clients)
        self.chat_manager = self.chat_manager()
        self.responses = responses
        self._lecture_creator = lecture_creator
        self._ws_active = ws_active

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

        if self._ws_active:
            for client in self.clients:
                # устанавливаем для каждого сообщения свой from_obj,
                # чтобы сериализатор в self.message_builder правильно определил собеседника в чате
                self.message_builder.from_obj = client
                message = WsMessage(type_=WsEventTypes.new_respondent, kwargs=self._get_message())
                sender = self.message_sender([client], message)
                sender.send()


class LectureCancelResponseWsService(WsService):
    def __init__(self, from_obj: User, clients: list[User], chat_id: int):
        super().__init__(from_obj, clients=clients)
        self.chat_id = chat_id

    def _get_message(self):
        return self.message_builder.remove_respondent(self.chat_id)

    def setup(self):
        message = WsMessage(type_=WsEventTypes.remove_respondent, kwargs=self._get_message())
        sender = self.message_sender(self.clients, message)
        sender.send()


class LectureConfirmRespondentWsService(WsService):
    chat_manager = ChatManager

    def _make_message_for_other_respondent(self, message: Message) -> WsMessage:
        built_message = self.message_builder.chat_message(message)
        built_message['confirm'] = True

        return WsMessage(type_=WsEventTypes.chat_message, kwargs=built_message)

    def send_message(self, message: Message, client: User = None) -> None:
        """ Создает и отправляет сообщение для откликнувшихся пользователей на подтвержденную дату """

        clients = client or self.clients  # если client передан,
        # то отправляем выбранному человеку, иначе self.clients

        ws_message = self._make_message_for_other_respondent(message)
        sender = self.message_sender(clients, ws_message)
        sender.send()

    def _make_delete_chat_message_for_other_respondent(self, chat_id: int) -> WsMessage:
        return WsMessage(
            type_=WsEventTypes.read_reject_chat, kwargs=self.message_builder.read_reject_chat(chat_id))

    def send_delete_chat_message_to_other_respondent(self, chat: Chat, client: User) -> None:
        """ Создает и отправляет сообщение для чата, который будет удален """

        ws_message = self._make_delete_chat_message_for_other_respondent(chat.pk)
        sender = self.message_sender([client], ws_message)
        sender.send()


class LectureRejectRespondentWsService(WsService):
    def _make_message(self, message: Message) -> WsMessage:
        built_message = self.message_builder.chat_message(message)
        built_message['confirm'] = False

        return WsMessage(type_=WsEventTypes.chat_message, kwargs=built_message)

    def send_message(self, message: Message) -> None:
        """ Создает и отправляет сообщение в чате """

        ws_message = self._make_message(message)
        sender = self.message_sender(self.clients, ws_message)
        sender.send()
