import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from speakers.settings import DEFAULT_HOST
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
        lecture_request = event['lecture_request']
        respondent = event['lecture_respondent']
        chat = await self.create_new_chat(event)
        need_read_messages = await self.get_need_read({**event, 'chat': chat})

        photo = None

        if hasattr(lecture_request, 'lecturer_lecture_request'):
            photo = lecture_request.lecturer_lecture_request.photo.url
        elif hasattr(lecture_request, 'customer_lecture_request'):
            photo = lecture_request.customer_lecture_request.photo.url

        data = {
            'type': 'new_respondent',
            'id': chat.pk,
            'need_read': need_read_messages,
            'lecture_name': lecture_request.lecture.name,
            'lecture_photo': DEFAULT_HOST + photo,
            'respondent_id': respondent.pk,
            'respondent_first_name': respondent.person.first_name,
            'respondent_last_name': respondent.person.last_name
        }
        await self.send(text_data=json.dumps(data))

    async def remove_respondent(self, event):
        chat_id = await self.remove_chat(event)
        await self.send(text_data=json.dumps(
            {
                'type': 'remove_respondent',
                'id': chat_id,
            }
        ))

    async def new_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def create_new_chat(self, data):
        chat = Chat.objects.filter(
            users__in=[data["lecture_creator"], data["lecture_respondent"]]).first()
        if not chat:
            chat = Chat.objects.create(lecture_request=data["lecture_request"])
            chat.users.add(data["lecture_creator"], data["lecture_respondent"])
            chat.save()

        Message.objects.get_or_create(
            author=data["lecture_respondent"],
            chat=chat,
            text='Добрый день! Мне подходит ваш запрос на проведение лекции!'
        )
        return chat

    @database_sync_to_async
    def get_need_read(self, data):
        if self.scope["url_route"]["kwargs"]["pk"] == data['lecture_respondent'].pk:
            return False
        return Message.objects.filter(
            chat=data['chat'], author=data['lecture_respondent'], need_read=True).exists()

    @database_sync_to_async
    def remove_chat(self, data):
        chat = Chat.objects.filter(
            lecture_request=data["lecture_request"],
            users=data["lecture_respondent"]
        ).first()
        chat_id = chat.pk
        chat.delete()
        return chat_id


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

        data = {
                'type': 'chat_message',
                'author': author,
                'chat_id': chat_id,
                'text': text
            }
        await self.create_new_message(data)
        recipient_pk = await self.get_recipient_id(author)
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

        await self.send(text_data=json.dumps({
            'author': author,
            'text': text
        }))

    @database_sync_to_async
    def create_new_message(self, data):
        messages = Message.objects.filter(chat_id=data['chat_id'])
        other_messages = messages.exclude(author=User.objects.get(pk=data['author']))
        for message in other_messages:
            message.need_read = False
            message.save()
        if messages.count() > 500:
            messages.first().delete()

        Message.objects.create(
            author=User.objects.get(pk=data['author']),
            chat=Chat.objects.get(pk=data['chat_id']),
            text=data['text']
        )

    @database_sync_to_async
    def get_recipient_id(self, author):
        return User.objects.filter(
            chat_list__id=self.scope["url_route"]["kwargs"]["pk"]).exclude(
            pk=author).first().pk
