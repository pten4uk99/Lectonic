from chatapp.models import Chat
from workroomsapp.models import Person


class ObjectManager:
    @staticmethod
    def get_chat(chat_id) -> Chat:
        return Chat.objects.filter(pk=chat_id).first()

    @staticmethod
    def get_person(person_id) -> Person:
        return Person.objects.filter(pk=person_id).first()
