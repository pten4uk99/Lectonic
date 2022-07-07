from services.base import Service
from services.db.lecture import ChatManager
from services.ws.base import WsService


class ChatService(Service):
    response_message_text = None
    ws_service: WsService = None
    object_manager = ChatManager

    def format_dates_for_message(self, *args, **kwargs) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        pass

    def make_message_text(self) -> str:
        """ Объединяет сообщение self.response_message_text и отформатированные даты лекции """

        dates = self.format_dates_for_message()
        str_dates = ", ".join(dates)
        return self.response_message_text + ' ' + str_dates

    def to_do(self) -> None:
        """ Собирает и запускает последовательно необходимые действия класса """
        pass

    def setup(self) -> None:
        """ Собирает и запускает последовательно необходимые действия класса """

        self.to_do()
        self.ws_service.setup()