from channels.db import database_sync_to_async

from authapp.models import User
from chatapp.models import Message, Chat


class DatabaseInteraction:
    @database_sync_to_async
    def create_new_chat(self, data):
        chat = Chat.objects.filter(
            users=data["lecture_respondent"], lecture=data["lecture"]).first()
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
        chat_id = data['chat_id']
        chat = Chat.objects.get(pk=chat_id)
        chat.delete()
        return chat_id

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
