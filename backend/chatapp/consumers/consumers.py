import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from chatapp.consumers.db import DatabaseInteraction
from chatapp.consumers.events import EventHandler

User = get_user_model()


class WsConsumer(AsyncWebsocketConsumer, DatabaseInteraction, EventHandler):
    async def connect(self):
        """ При новом подключении добавляем идентификатор канала в
        группу common (общая группа для всех участников соединения) и
        создаем в базе объект WsClient, который связывает пользователя с идентификатором канала """

        await self.channel_layer.group_add('common', self.channel_name)

        await self.add_ws_client(
            user_id=self.scope["url_route"]["kwargs"]["pk"],
            channel_name=self.channel_name
        )
        await self.channel_layer.group_send('common', {'type': 'set_online_users'})
        await self.accept()

    async def disconnect(self, code):
        """ При дисконнекте удаляем канал из группы common и
        удаляем объект WsClient с текущим каналом из БД """

        await self.channel_layer.group_discard('common', self.channel_name)

        await self.remove_ws_client(channel_name=self.channel_name)
        await self.channel_layer.group_send('common', {'type': 'set_online_users'})

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        if data['type'] == 'chat_message':
            await self.handle_chat_message(data)
        elif data['type'] == 'read_reject_chat':
            await self.handle_read_reject_chat(data)

    async def handle_chat_message(self, data):
        recipient_pk = await self.get_recipient_id(data)  # берем id получателя сообщения
        recipient_client = await self.get_ws_client(user_id=recipient_pk)  # получаем объект WsClient
        author_client = await self.get_ws_client(user_id=data['author'])
        message = await self.create_new_message(data)

        data['datetime'] = str(message.datetime)
        data['confirm'] = message.confirm
        data['need_read'] = message.need_read

        await self.channel_layer.send(getattr(recipient_client, 'channel_name', 'None'), data)
        await self.channel_layer.send(getattr(author_client, 'channel_name', 'None'), data)

    async def handle_read_reject_chat(self, data):
        chat_id = data['chat_id']
        clients = await self.get_ws_clients_from_chat(chat_id)

        if len(clients) > 0:
            await self.channel_layer.send(clients[0].channel_name, data)
            if len(clients) > 1:
                await self.channel_layer.send(clients[1].channel_name, data)
