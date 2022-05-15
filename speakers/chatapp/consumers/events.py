import json
import logging

logger = logging.getLogger(__name__)


class EventHandler:
    async def set_online_users(self, event):
        users = await self.get_all_clients()
        event['users'] = users
        await self.send(text_data=json.dumps(event))

    async def new_respondent(self, event):
        talker = await self.get_talker(event)
        need_read_messages = await self.get_need_read_messages(event)

        data = {
            'type': 'new_respondent',
            **event,
            'need_read': need_read_messages,
            'talker_first_name': talker.first_name,
            'talker_last_name': talker.last_name,
        }
        logger.info(f'new_respondent_data: {data}')
        await self.send(text_data=json.dumps(data))

    async def remove_respondent(self, event):
        chat_id = event['chat_id']
        await self.send(text_data=json.dumps(
            {
                'type': 'remove_respondent',
                'id': chat_id,
            }
        ))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def read_messages(self, event):
        await self.send(text_data=json.dumps(event))

    async def read_reject_chat(self, event):
        chat_id = await self.remove_chat(event)
        await self.send(text_data=json.dumps({
            'type': 'read_reject_chat',
            'response': 'deleted',
            'chat_id': chat_id
        }))
