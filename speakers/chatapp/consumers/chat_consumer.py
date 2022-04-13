import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from speakers.settings import DEFAULT_HOST
from chatapp.models import Message, Chat

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
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
        text_data_json = json.loads(text_data)
        author = text_data_json['author']
        chat_id = self.scope["url_route"]["kwargs"]["pk"]
        text = text_data_json['text']
        confirm = text_data_json.get('confirm')

        data = {
            'type': 'chat_message',
            'author': author,
            'chat_id': chat_id,
            'text': text,
            'confirm': confirm
        }

        recipient_pk = await self.get_recipient_id(author)
        await self.create_new_message(data)
        await self.channel_layer.group_send(
            f'chat_{self.scope["url_route"]["kwargs"]["pk"]}', data)
        await get_channel_layer().group_send(
            f'user_{recipient_pk}', {
                'type': 'new_message',
                'chat_id': chat_id
            })

    async def chat_message(self, event):
        author = event['author']
        text = event['text']
        confirm = event.get('confirm')

        await self.send(text_data=json.dumps({
            'author': author,
            'text': text,
            'confirm': confirm
        }))

    @database_sync_to_async
    def create_new_message(self, data):
        messages = Message.objects.filter(chat_id=self.scope["url_route"]["kwargs"]["pk"])
        other_messages = messages.exclude(author=User.objects.get(pk=data['author']))
        for message in other_messages:
            message.need_read = False
            message.save()
        if messages.count() > 500:
            messages.first().delete()

        Message.objects.create(
            author=User.objects.get(pk=data['author']),
            chat=Chat.objects.get(pk=self.scope["url_route"]["kwargs"]["pk"]),
            text=data['text'],
            confirm=data.get('confirm')
        )

    @database_sync_to_async
    def get_recipient_id(self, author):
        return User.objects.filter(
            chat_list__id=self.scope["url_route"]["kwargs"]["pk"]).exclude(
            pk=author).first().pk
