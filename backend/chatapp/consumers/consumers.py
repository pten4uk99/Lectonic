import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from chatapp.consumers.db import DatabaseInteraction
from chatapp.consumers.events import EventHandler, set_online_users
from chatapp.consumers.handlers import handle_client_side_message
from services.types import WsEventTypes, WsGroups

User = get_user_model()


def bind_message_type(name):
    def decorator(func):
        async def wrapper(data):
            data['type'] = name
            return await func(data)

        return wrapper

    return decorator


class WsConsumer(AsyncWebsocketConsumer, DatabaseInteraction, EventHandler):
    def __new__(cls, *args, **kwargs):
        for event in WsEventTypes:
            setattr(cls, event.value, event.value)
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for event in WsEventTypes:
            setattr(self, event.value, bind_message_type(event.value)(self._handle_event))

    async def _handle_event(self, data):
        await self.send(text_data=json.dumps(data))

    async def connect(self):
        await self.channel_layer.group_add(WsGroups.common.value, self.channel_name)
        await set_online_users(user_id=self.scope["url_route"]["kwargs"]["pk"], channel_name=self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(WsGroups.common.value, self.channel_name)
        await set_online_users(
            user_id=self.scope["url_route"]["kwargs"]["pk"], channel_name=self.channel_name, remove=True)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await handle_client_side_message(data)

    async def handle_chat_message(self, data):
        recipient_pk = await self.get_recipient_id(data)  # берем id получателя сообщения
        recipient_client = await self.get_ws_client(user_id=recipient_pk)  # получаем объект WsClient
        author_client = await self.get_ws_client(user_id=data['author'])
        message = await self.create_new_message(data)

        data['datetime'] = str(message.datetime)
        data['confirm'] = message.confirm
        data['need_read'] = message.need_read

        await self.channel_layer.send(getattr(recipient_client, 'channel_name', 'None'), data)
        await self.channel_layer.send(getattr(author_client, 'channel_name', 'None'), data)
