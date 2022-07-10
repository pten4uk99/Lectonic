from typing import Type

from rest_framework.exceptions import APIException

from services.types import WsEventTypes
from .events import *

EVENTS = [ChatMessageEvent, ReadRejectChatEvent]


class MessageTypeException(APIException):
    """ Ошибка получения типа сообщения вебсокета """


class ClientSideTypeMessageHandler:
    """ Обрабатывает сообщения переданные в метод receive() вебсокет-консьюмера """

    event_types = WsEventTypes

    def __init__(self, message: dict):
        self.message = message
        self.message_type = self.get_message_type(message)

    @staticmethod
    def get_message_type(message: dict) -> str:
        try:
            return message['type']
        except KeyError:
            raise MessageTypeException("В обработчик не передан тип сообщения")

    def _appoint_event_handler(self) -> Type:
        for event in EVENTS:
            if self.message_type == event.type_.value:
                return event

    def _check_type_exist(self) -> bool:
        """ Проверяет существует ли такое событие """

        return hasattr(self.event_types, self.message_type)

    async def handle(self):
        if self._check_type_exist():
            event_class = self._appoint_event_handler()
            event = event_class(self.message)
            await event.setup()


# функции вызывающиеся снаружи файла
async def handle_client_side_message(data: dict):
    handler = ClientSideTypeMessageHandler(data)
    await handler.handle()
