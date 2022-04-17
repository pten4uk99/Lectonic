import json


class NotificationEventHandler:
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
        chat_id = event['chat_id']
        await self.send(text_data=json.dumps(
            {
                'type': 'remove_respondent',
                'id': chat_id,
            }
        ))

    async def new_message(self, event):
        print('we are here')
        await self.send(text_data=json.dumps(event))
