from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from chatapp import chatapp_responses
from chatapp.models import Chat, Message
from services.base import Service
from services.db.chat import ChatMessageObjectManager
from services.ws.chatapp import ChatMessageWsService
from services.types import AttrNames


class ChatMessageService(Service):
    object_manager = ChatMessageObjectManager
    ws_service = ChatMessageWsService

    def __init__(self, from_obj: User, chat_id: int, from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj, from_attr)
        self.chat = self._get_chat(chat_id)
        self.chat_messages = self._get_chat_messages()

        self._to_do_ran = False

        clients = list(self.chat.users.all())
        self.ws_service = self.ws_service(from_obj=from_obj, chat=self.chat, clients=clients)

    def _get_chat(self, chat_id) -> Chat:
        chat = self.object_manager.get_chat(chat_id)

        if not chat:
            return chatapp_responses.chat_does_not_exist()
        return chat

    def _get_chat_messages(self) -> QuerySet[Message]:
        return self.object_manager.get_chat_messages(self.chat)

    def _read_other_messages(self) -> None:
        """ Делает все сообщения собеседника прочитанными """

        other_messages = self.chat_messages.exclude(author=self.from_obj)  # сообщения собеседника

        for message in other_messages:
            self.object_manager.set_message_need_read(message, need_read=False)

    def _to_do(self):
        if not self._to_do_ran:
            self._read_other_messages()
            self.ws_service.setup()

            self._to_do_ran = True

    def setup(self):
        self._to_do()
