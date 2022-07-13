from enum import Enum

from authapp.models import User
from chatapp.models import Chat, Message
from services.base import Service
from services.db.lecture import ChatManager
from services.ws.base import WsService


class SystemMessageForAuthorText(Enum):
    confirm_lecture: str = 'Лекция подтверждена!'
    reject_lecture: str = 'Лекция отклонена!'
    lecture_response: str = 'Вы отправили запрос. ' \
                            'Возможные даты проведения:'


class SystemMessageForRecipientText(Enum):
    confirm_lecture: str = 'Лекция подтверждена!'
    reject_lecture: str = 'Лекция отклонена!'
    lecture_response: str = 'Собеседник заинтересован в Вашем предложении. ' \
                            'Возможные даты проведения:'
    confirm_respondent: str = f'Одна или более из выбранных вами дат на данную лекцию ' \
                              f'уже подтверждена для другого пользователя. ' \
                              f'Возможные даты проведения:'


class ChatService(Service):
    ws_service: WsService = None
    object_manager = ChatManager

    def format_dates_for_message(self, *args, **kwargs) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        pass

    def to_do(self) -> None:
        """ Собирает и запускает последовательно необходимые действия класса """
        pass

    def setup(self) -> None:
        """ Собирает и запускает последовательно необходимые действия класса """

        self.to_do()
        self.ws_service.setup()


class CurrentChatMessagesChatService(ChatService):
    message_for_author: SystemMessageForAuthorText = None
    message_for_recipient: SystemMessageForRecipientText = None

    def build_message_for_author(self) -> str:
        """ Дополнительный обработчик сообщения для автора """

        return self.message_for_author.value

    def build_message_for_recipient(self) -> str:
        """ Дополнительный обработчик сообщения для получателя """

        return self.message_for_recipient.value

    def send_ws_message(self, message: Message, client: User) -> None:
        """ Срабатывает сразу после создания сообщения """

    def create_current_chat_messages(self, chat: Chat):
        """ Создает сообщения для пользователей текущего чата """

        #  Чтобы оба сообщения не дублировались в один чат,
        #  системные сообщения в чат должны приходить только от собеседника:
        #  то есть, если сообщение предназначено для откликнувшегося,
        #  то оно должно приходить от создателя лекции, и наоборот.
        author = self.object_manager.get_user_from_chat(chat, exclude_user=self.from_obj)
        author_message = self.object_manager.create_message(
            chat=chat,
            author=author,
            system_text=self.build_message_for_author()
        )
        self.send_ws_message(author_message, client=self.from_obj)

        recipient_message = self.object_manager.create_message(
            chat=chat,
            author=self.from_obj,
            system_text=self.build_message_for_recipient()
        )
        self.send_ws_message(recipient_message, client=author)
