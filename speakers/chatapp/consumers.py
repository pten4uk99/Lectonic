import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Message, Chat

User = get_user_model()


class NotificationsConsumer(AsyncWebsocketConsumer):
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

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(f'user_{self.scope["url_route"]["kwargs"]["pk"]}',
                                            {'type': 'notification',
                                                'message': 'рпривет'})
        print(text_data_json)

    async def new_respondent(self, event):
        await self.create_new_chat(event)
        await self.send(text_data=json.dumps({'message': 'чатик создан'}))

    async def remove_respondent(self, event):
        await self.remove_chat(event)
        await self.send(text_data=json.dumps({'message': 'чатик удален'}))

    @database_sync_to_async
    def create_new_chat(self, data):
        chat = Chat.objects.create(lecture_request=data["lecture_request"])
        chat.users.add(data["lecture_creator"], data["lecture_respondent"])
        chat.save()

    @database_sync_to_async
    def remove_chat(self, data):
        Chat.objects.filter(
            lecture_request=data["lecture_request"],
            users=data["lecture_respondent"]
        ).delete()



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add(
            'users',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            'users',
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        current_user = text_data_json['current_user']
        other_user = text_data_json['other_user']
        chat_id = text_data_json['chat_id']
        message = text_data_json['message']

        data = {
                'type': 'chat_message',
                'current_user': current_user,
                'other_user': other_user,
                'chat_id': chat_id,
                'message': message
            }
        # await self.create_new_message(data)
        await self.channel_layer.group_send('users', data)

    async def chat_message(self, event):
        current_user = event['current_user']
        other_user = event['other_user']
        chat_id = event['chat_id']
        message = event['message']

        await self.send(text_data=json.dumps({
            'current_user': current_user,
            'other_user': other_user,
            'chat_id': chat_id,
            'message': message
        }))

    @database_sync_to_async
    def create_new_message(self, data):
        Message.objects.create(
            author=User.objects.get(pk=data['current_user']),
            chat=Chat.objects.get(pk=data['chat_id']),
            text=data['message']
        )