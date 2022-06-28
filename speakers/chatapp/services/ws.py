from django.http import HttpRequest

from authapp.models import User
from chatapp.models import Chat
from chatapp.services.ws_message import WsMessage, WsEventTypes
from workroomsapp.lecture.services.ws import WsService


class ChatMessageWsService(WsService):
    def __init__(self, request: HttpRequest, from_obj: User, chat: Chat, clients: list[User]):
        super().__init__(request, from_obj, clients=clients)
        self.chat = chat

    def _get_message(self):
        self.message_builder.read_messages(self.chat)

    def setup(self):
        ws_message = WsMessage(type_=WsEventTypes.read_messages, kwargs=self._get_message())
        sender = self.message_sender(self.clients, ws_message)
        sender.send()
