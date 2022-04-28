import json


class EventHandler:
    async def new_respondent(self, event):
        lecture = event['lecture']
        respondent = event['lecture_respondent'].person
        # chat = await self.create_new_chat(event)
        chat = event['chat']
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
        chat_id = event['chat_id']
        await self.send(text_data=json.dumps(
            {
                'type': 'remove_respondent',
                'id': chat_id,
            }
        ))

    # для чата ->
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
