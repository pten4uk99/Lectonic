from django.http import HttpRequest

from chatapp.chatapp_serializers import ChatSerializer
from chatapp.models import Chat
from dataclasses import dataclass
from enum import Enum

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from chatapp.models import WsClient


class WsEventTypes(Enum):
    new_respondent = 'new_respondent'
    set_online_users = 'set_online_users'
    remove_respondent = 'remove_respondent'
    chat_message = 'chat_message'
    read_messages = 'read_messages'
    read_reject_chat = 'read_reject_chat'


@dataclass
class WsMessage:
    type_: WsEventTypes
    kwargs: dict

    def to_dict(self):
        return {'type': self.type_.value, **self.kwargs}


class WsMessageSender:
    channel_layer = get_channel_layer()

    def __init__(self, clients: list, message: WsMessage):
        self.message = message.to_dict()
        self.clients = WsClient.objects.filter(user__in=clients)

    def send(self) -> None:
        """ Отправляет вебсокет сообщение """

        for client in self.clients:
            async_to_sync(self.channel_layer.send)(getattr(client, 'channel_name', ''), self.message)


class WsMessageBuilder:
    def __init__(self, request: HttpRequest):
        self.request = request

    def new_respondent(self, chat: Chat) -> dict:
        """ Сериализует сообщение для вебсокета в json """

        serializer = ChatSerializer(chat, context={'request': self.request})
        return {
            'respondent_id': self.request.user.pk,
            **serializer.data
        }
