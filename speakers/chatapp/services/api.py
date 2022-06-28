from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from chatapp import chatapp_responses
from chatapp.chatapp_serializers import MessageListSerializer
from chatapp.models import Chat, Message
from chatapp.services.db import ChatMessageObjectManager
from chatapp.services.ws import ChatMessageWsService
from speakers.service import Service
from workroomsapp.lecture.services.db import AttrNames


class ChatMessageAPI(Service):
    object_manager = ChatMessageObjectManager
    serializer_class = MessageListSerializer
    ws_service = ChatMessageWsService

    def __init__(self, request: HttpRequest, from_obj: User, chat_id: int, from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj, from_attr)
        self.chat = self._get_chat(chat_id)
        self.chat_messages = self._get_chat_messages()

        self._to_do_ran = False

        self.ws_service = self.ws_service(
            request, from_obj=from_obj, chat=self.chat, clients=self.chat.users.all())

    def _get_chat(self, chat_id) -> Chat:
        chat = self.object_manager.get_chat(chat_id)

        if not chat:
            return chatapp_responses.chat_does_not_exist()
        return chat

    def _get_chat_messages(self) -> QuerySet[Message]:
        return self.object_manager.get_chat_messages(self.chat)

    def _read_other_messages(self) -> None:
        """ Делает все сообщения собеседника прочитанными """

        other_messages = self.chat_messages.exclude(author=self.from_obj)  # сообщения собеседника

        for message in other_messages:
            self.object_manager.set_message_need_read(message, need_read=True)

    def _to_do(self):
        if not self._to_do_ran:
            self._read_other_messages()
            self.ws_service.setup()

            self._to_do_ran = True

    def serialize(self):
        self._to_do()
        return self.serializer_class(self.chat_messages, many=True, context={'user': self.from_obj})


# функции для использования непосредственно в представлениях
def serialize_chat_message_list(request: HttpRequest, chat_id: int):
    return ChatMessageAPI(from_obj=request.user, chat_id=chat_id).serialize()
