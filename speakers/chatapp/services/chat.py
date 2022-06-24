from django.db.models import QuerySet

from authapp.models import User
from chatapp.models import Chat
from speakers.service import Service
from workroomsapp.lecture.services.db import AttrNames, ChatManager
from workroomsapp.models import Lecture, LectureRequest, Person


class ChatService(Service):
    def setup(self) -> None:
        """ Собирает и запускает последовательно необходимые действия класса """
        pass


class LectureResponseChatService(ChatService):
    response_message_text = 'Собеседник заинтересован в Вашем предложении. ' \
                            'Возможные даты проведения:'
    object_manager = ChatManager

    def __init__(self, from_obj: User, lecture: Lecture,
                 responses: QuerySet[LectureRequest], lecture_creator: Person,
                 from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj, from_attr)
        self._lecture = lecture
        self._lecture_responses = responses
        self._lecture_creator = lecture_creator

    def _format_dates_for_message(self) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        dates = []

        for response in self._lecture_responses:
            dates.append(response.event.datetime_start.strftime('%d.%m'))

        return dates

    def _make_response_message_text(self) -> str:
        """ Объединяет сообщение self.response_message_text и отформатированные даты лекции """

        dates = self._format_dates_for_message()
        str_dates = ", ".join(dates)
        return self.response_message_text + ' ' + str_dates

    def _create_chat(self) -> Chat:
        """ Возвращает объект Chat по переданным датам """

        responses = self._lecture_responses
        chat = self.object_manager.get_chat_by_dates(
            dates=responses, creator=self._lecture_creator.user, respondent=self.from_obj)

        if not chat:
            chat = self.object_manager.create_chat(self._lecture)
            self.object_manager.add_responses(chat, responses, save=False)
            self.object_manager.add_users(
                chat, creator=self._lecture_creator.user, respondent=self.from_obj, save=False)
            chat.save()

        # logger.info(f'chat: {chat}')
        return chat

    def _create_response_message(self) -> None:
        """ Создает в чате стандартное сообщение при отклике """

        message = self.object_manager.create_message(
            self._create_chat(), self.from_obj, self._make_response_message_text())

        # logger.info(f'text:{message.text}, author: {message.author}')

    def setup(self) -> None:
        """ Создает новый чат (если его до этого не существовало) и
        стандартное сообщение в чате при отклике """

        self._create_chat()
        self._create_response_message()


class LectureCancelResponseChatService(ChatService):
    object_manager = ChatManager

    def __init__(self, from_obj: User, chat: Chat):
        super().__init__(from_obj)
        self._chat = chat

    def _remove_chat(self) -> None:
        self.object_manager.delete_chat(self._chat)

    def setup(self):
        self._remove_chat()
