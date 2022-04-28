from channels.db import database_sync_to_async

from authapp.models import User
from chatapp.models import Message, Chat, WsClient


class DatabaseInteraction:
    @database_sync_to_async
    def add_ws_client(self, user_id, channel_name):
        client = WsClient.objects.filter(user_id=user_id).first()

        if client:
            client.channel_name = channel_name
            client.save()
        else:
            client = WsClient.objects.create(channel_name=channel_name, user_id=user_id)

        return client

    @database_sync_to_async
    def remove_ws_client(self, channel_name):
        return WsClient.objects.get(channel_name=channel_name).delete()

    @database_sync_to_async
    def get_ws_client(self, channel_name=None, user_id=None):
        if user_id is not None:
            client = WsClient.objects.filter(user_id=user_id).first()
        elif channel_name is not None:
            client = WsClient.objects.filter(channel_name=channel_name).first()
        else:
            raise AttributeError('В функцию должен быть передан хотя бы один аргумент')
        return client



    @database_sync_to_async
    def create_new_chat(self, data):
        chat = Chat.objects.filter(
            lecture_requests__in=data["lecture_requests"]).first()
        if not chat:
            chat = Chat.objects.create(lecture=data["lecture"])
            chat.lecture_requests.add(data["lecture_requests"])
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
        chat_id = data['chat_id']
        chat = Chat.objects.get(pk=chat_id)
        chat.delete()
        return chat_id

    @database_sync_to_async
    def create_new_message(self, data):
        messages = Message.objects.filter(chat_id=data['chat_id'])
        other_messages = messages.exclude(author=User.objects.get(pk=data['author']))
        for message in other_messages:
            message.need_read = False
            message.save()
        if messages.count() > 500:
            messages.first().delete()

        return Message.objects.create(
            author=User.objects.get(pk=data['author']),
            chat=Chat.objects.get(pk=data['chat_id']),
            text=data['text'],
            confirm=data.get('confirm')
        )

    @database_sync_to_async
    def get_recipient_id(self, data):
        return User.objects.filter(
            chat_list__id=data['chat_id']).exclude(
            pk=data['author']).first().pk
