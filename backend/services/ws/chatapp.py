from django.http import HttpRequest

from authapp.models import User
from chatapp.models import Chat
from services.types import WsEventTypes
from services.ws.ws_message import WsMessage
from services.ws.base import WsService


class ChatMessageWsService(WsService):
    def __init__(self, from_obj: User, chat: Chat, clients: list[User]):
        super().__init__(from_obj, clients=clients)
        self.chat = chat

    def _get_message(self):
        return self.message_builder.read_messages(self.chat.pk)

    def setup(self):
        ws_message = WsMessage(type_=WsEventTypes.read_messages, kwargs=self._get_message())
        sender = self.message_sender(self.clients, ws_message)
        sender.send()
