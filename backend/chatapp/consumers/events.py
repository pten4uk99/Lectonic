import json
import logging
from abc import abstractmethod

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.db.models import QuerySet

from authapp.models import User
from chatapp.models import Chat, Message, WsClient
from services.db import ChatManager
from services.types import ChatMessageEventType, WsEventTypes, WsGroups, user_id_type, ReadRejectChatEventType

logger = logging.getLogger(__name__)

__all__ = [
    'WsEvent',
    'ChatMessageEvent',
    'ReadRejectChatEvent',
    'SetOnlineUsersEvent',

    'set_online_users',
]


class EventHandler:
    pass
    # async def set_online_users(self, event):
    #     users = await self.get_all_clients()
    #     event['users'] = users
    #     await self.send(text_data=json.dumps(event))

    # async def new_respondent(self, event):
    #     talker = await self.get_talker(event)
    #     need_read_messages = await self.get_need_read_messages(event)
    #
    #     data = {
    #         'type': 'new_respondent',
    #         **event,
    #         'need_read': need_read_messages,
    #         'talker_first_name': talker.first_name,
    #         'talker_last_name': talker.last_name,
    #     }
    #     logger.info(f'new_respondent_data: {data}')
    #     await self.send(text_data=json.dumps(data))
    #
    # async def remove_respondent(self, event):
    #     chat_id = event['chat_id']
    #     await self.send(text_data=json.dumps(
    #         {
    #             'type': 'remove_respondent',
    #             'id': chat_id,
    #         }
    #     ))

    # async def chat_message(self, event):
    #     await self.send(text_data=json.dumps(event))

    # async def read_messages(self, event):
    #     await self.send(text_data=json.dumps(event))

    # async def read_reject_chat(self, event):
    #     chat_id = await self.remove_chat(event)
    #     await self.send(text_data=json.dumps({
    #         'type': 'read_reject_chat',
    #         'response': 'deleted',
    #         'chat_id': chat_id
    #     }))


class WsEvent:
    """ Обязательно надо указать type_ """
    channel_layer = get_channel_layer()
    type_: str = None
    object_manager = ChatManager

    def __init__(self):
        self.object_manager = self.object_manager()

    def __str__(self):
        return self.type_

    @abstractmethod
    async def send(self, *args, **kwargs) -> None:
        """ Отправляет вебсокет сообщение """

    @abstractmethod
    async def setup(self) -> None:
        """ Обрабатывает вебсокет-сообщение """


class SetOnlineUsersEvent(WsEvent):
    type_ = WsEventTypes.set_online_users

    def __init__(self, user_id: int, channel_name: str, remove: bool = False):
        super().__init__()
        self.user_id = user_id
        self.channel_name = channel_name
        self.remove = remove

    @database_sync_to_async
    def _get_all_clients(self) -> list[user_id_type]:
        clients = WsClient.objects.all().values_list('user', flat=True)
        return list(clients)

    @database_sync_to_async
    def _add_ws_client(self) -> WsClient:
        client = WsClient.objects.filter(user_id=self.user_id).first()

        if client:
            client.channel_name = self.channel_name
            client.save()
        else:
            client = WsClient.objects.create(channel_name=self.channel_name, user_id=self.user_id)

        return client

    @database_sync_to_async
    def _remove_ws_client(self):
        return WsClient.objects.filter(channel_name=self.channel_name).delete()

    async def _execute(self):
        """ Проверяет нужно ли удалять объект WsClient.
        Если нужно - удаляет, иначе создает новый """

        if self.remove:
            await self._remove_ws_client()
        else:
            await self._add_ws_client()

    async def send(self):
        clients: list[user_id_type] = await self._get_all_clients()
        await self.channel_layer.group_send(
            WsGroups.common.value, {'type': WsEventTypes.set_online_users.value, 'users': clients})

    async def setup(self):
        await self._execute()
        await self.send()


class ReadRejectChatEvent(WsEvent):
    type_ = WsEventTypes.read_reject_chat

    def __init__(self, data: ReadRejectChatEventType):
        super().__init__()
        self.data = data

    @database_sync_to_async
    def remove_chat(self):
        chat = Chat.objects.filter(pk=self.data['chat_id']).first()
        if chat:
            chat.delete()

    @database_sync_to_async
    def get_ws_clients_from_chat(self) -> list[WsClient]:
        clients = []
        chat = Chat.objects.filter(pk=self.data['chat_id']).first()

        if chat:
            for user in chat.users.all():
                client: WsClient = getattr(user, 'ws_client', None)
                if client:
                    clients.append(client)

        return clients

    async def send(self):
        clients = await self.get_ws_clients_from_chat()

        # после тестов постараться убрать добавление этого ключа!!!
        self.data['response'] = 'deleted'
        # после тестов постараться убрать добавление этого ключа!!!

        if len(clients) > 0:
            for client in clients:
                await self.channel_layer.send(client.channel_name, self.data)

    async def setup(self):
        await self.send()
        await self.remove_chat()


class ChatMessageEvent(WsEvent):
    """ Событие сообщения в чате """

    type_ = WsEventTypes.chat_message
    data_type = ChatMessageEventType

    def __init__(self, data: dict):
        super().__init__()
        self.data = self._normalize_data(data)

    def _normalize_data(self, data: dict) -> ChatMessageEventType:
        if 'need_read' not in data:
            data['need_read'] = True

        return self.data_type(**data)

    @database_sync_to_async
    def _read_messages(self, messages: QuerySet[Message]) -> None:
        for message in messages:
            self.object_manager.read_message(message)

    @database_sync_to_async
    def _handle_messages_count(self, messages: QuerySet[Message]) -> None:
        if self.object_manager.count_messages(messages) > 500:
            self.object_manager.delete_first_message(messages)

    @database_sync_to_async
    def _create_new_message(self, chat: Chat) -> Message:
        author = self.object_manager.get_object_by_id(User, self.data['author'])

        return self.object_manager.create_message(
            chat=chat,
            author=author,
            text=self.data['text'],
        )

    async def send(self, chat: Chat) -> None:
        message_author: User = await database_sync_to_async(
            self.object_manager.get_object_by_id)(User, self.data['author'])
        recipient: User = await database_sync_to_async(
            self.object_manager.get_user_from_chat)(chat, exclude_user=message_author)

        recipient_client: WsClient = await database_sync_to_async(
            self.object_manager.get_ws_client)(user_id=recipient.pk)
        author_client: WsClient = await database_sync_to_async(
            self.object_manager.get_ws_client)(user_id=message_author.pk)

        await self.channel_layer.send(getattr(recipient_client, 'channel_name', 'None'), self.data)
        await self.channel_layer.send(getattr(author_client, 'channel_name', 'None'), self.data)

    async def setup(self):
        """
        1. Проверяет, чтобы количество сообщений в чате не превышало 500.
        2. Помечает прочитанными сообщения собеседника.
        3. Создает новое сообщение из переданных данных.
        4. Отправляет сообщение.
         """

        messages: QuerySet[Message] = await database_sync_to_async(
            self.object_manager.get_messages_by_chat)(self.data['chat_id'])
        other_messages: QuerySet[Message] = await database_sync_to_async(
            self.object_manager.exclude_user_in_messages)(messages, self.data['author'])
        chat = await database_sync_to_async(
            self.object_manager.get_object_by_id)(Chat, self.data['chat_id'])

        await self._handle_messages_count(messages)
        await self._read_messages(other_messages)
        await self._create_new_message(chat)
        await self.send(chat)


# ----------------функции для внешнего мира-----------------------
async def set_online_users(user_id: int, channel_name: str, remove: bool = False):
    event = SetOnlineUsersEvent(user_id=user_id, channel_name=channel_name, remove=remove)
    await event.setup()
