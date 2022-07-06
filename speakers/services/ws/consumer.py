from chatapp.consumers.db import DatabaseInteraction


class ConsumerService:
    db_manager = DatabaseInteraction

    async def connect(self):
        pass
