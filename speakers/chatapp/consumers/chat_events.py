import json


class ChatEventHandler:
    async def chat_message(self, event):
        author = event['author']
        text = event['text']
        confirm = event.get('confirm')

        await self.send(text_data=json.dumps({
            'author': author,
            'text': text,
            'confirm': confirm
        }))

    async def read_reject_chat(self, event):
        chat_id = await self.remove_chat(event)
        await self.send(text_data=json.dumps({
            'type': 'read_reject_chat',
            'response': 'deleted',
            'chat_id': chat_id
        }))
