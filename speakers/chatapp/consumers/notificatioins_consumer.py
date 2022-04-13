import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from speakers.settings import DEFAULT_HOST
from chatapp.models import Message, Chat

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

    async def new_respondent(self, event):
        lecture = event['lecture']
        respondent = event['lecture_respondent'].person
        chat = await self.create_new_chat(event)
        need_read_messages = await self.get_need_read({**event, 'chat': chat})

        data = {
            'type': 'new_respondent',
            'id': chat.pk,
            'need_read': need_read_messages,
            'lecture_name': lecture.name,
            'lecture_svg': lecture.svg,
            'respondent_id': respondent.pk,
            'respondent_first_name': respondent.first_name,
            'respondent_last_name': respondent.last_name
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
            chat = Chat.objects.create(lecture=data["lecture"])
            chat.users.add(data["lecture_creator"], data["lecture_respondent"])
            chat.save()

        dates = []
        for date in data["dates"]:
            dates.append(date.strftime('%d.%m'))

        Message.objects.get_or_create(
            author=data["lecture_respondent"],
            chat=chat,
            text=f'Собеседник заинтересован в Вашем предложении. '
                 f'Возможные даты проведения: {", ".join(dates)}.'
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
            lecture=data["lecture"],
            users=data["lecture_respondent"]
        ).first()
        chat_id = chat.pk
        chat.delete()
        return chat_id
