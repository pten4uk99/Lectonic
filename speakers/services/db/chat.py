from django.db.models import QuerySet

from chatapp.models import Message, Chat
from speakers.db import ObjectManager
from services.types import AttrNames


class ChatMessageObjectManager(ObjectManager):
    def __init__(self, from_attr: AttrNames = AttrNames.LECTURER):
        self.from_attr = from_attr

    @staticmethod
    def get_chat_messages(chat: Chat) -> QuerySet[Message]:
        return Message.objects.order_by('datetime').filter(chat=chat)

    @staticmethod
    def set_message_need_read(message: Message, need_read: bool):
        message.need_read = need_read
        message.save()
