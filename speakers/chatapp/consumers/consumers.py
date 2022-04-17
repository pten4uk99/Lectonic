import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from chatapp.consumers.chat_events import ChatEventHandler
from chatapp.consumers.db import DatabaseInteraction
from chatapp.consumers.notifications_events import NotificationEventHandler

User = get_user_model()


class NotificationsConsumer(AsyncWebsocketConsumer,
                            DatabaseInteraction,
                            NotificationEventHandler):
    async def connect(self):
        await self.channel_layer.group_add(
            f'user_{self.scope["url_route"]["kwargs"]["pk"]}',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f'user_{self.scope["url_route"]["kwargs"]["pk"]}',
            self.channel_name
        )


class ChatConsumer(AsyncWebsocketConsumer,
                   DatabaseInteraction,
                   ChatEventHandler):
    async def connect(self):
        await self.channel_layer.group_add(
            f'chat_{self.scope["url_route"]["kwargs"]["pk"]}',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f'chat_{self.scope["url_route"]["kwargs"]["pk"]}',
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        data['chat_id'] = self.scope["url_route"]["kwargs"]["pk"]

        if data['type'] == 'chat_message':
            await self.handle_chat_message(data)
        else:
            await self.channel_layer.group_send(
                f'chat_{self.scope["url_route"]["kwargs"]["pk"]}', data)

    async def handle_chat_message(self, data):
        recipient_pk = await self.get_recipient_id(data['author'])
        await self.create_new_message(data)
        await self.channel_layer.group_send(
            f'chat_{self.scope["url_route"]["kwargs"]["pk"]}', data)
        await get_channel_layer().group_send(
            f'user_{recipient_pk}', {
                'type': 'new_message',
                'chat_id': data['chat_id']
            })