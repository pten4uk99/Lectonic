from django.http import HttpRequest

from authapp.models import User
from services.base import Service
from .ws_message import WsMessageBuilder, WsMessageSender


class WsService(Service):
    message_builder = WsMessageBuilder
    message_sender = WsMessageSender

    def __init__(self, from_obj: User, clients: list[User]):
        super().__init__(from_obj)
        self.message_builder = self.message_builder(from_obj)
        self.clients = clients

    def _get_message(self) -> dict:
        """ Возвращает сообщение для вебсокета """
        pass

    def setup(self) -> None:
        """ Собирает и запускает последовательно необходимые действия класса """
        pass