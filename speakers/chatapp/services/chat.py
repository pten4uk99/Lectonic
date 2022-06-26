from django.db.models import QuerySet

from authapp.models import User
from chatapp.models import Chat
from chatapp.services.ws import DeletedChat
from speakers.service import Service
from workroomsapp.lecture.services.db import AttrNames, ChatManager
from workroomsapp.models import Lecture, LectureRequest, Person


class ChatService(Service):
    response_message_text = None

    def format_dates_for_message(self, *args, **kwargs) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        pass

    def make_message_text(self) -> str:
        """ Объединяет сообщение self.response_message_text и отформатированные даты лекции """

        dates = self.format_dates_for_message()
        str_dates = ", ".join(dates)
        return self.response_message_text + ' ' + str_dates

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

    def format_dates_for_message(self) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        dates = []

        for response in self._lecture_responses:
            dates.append(response.event.datetime_start.strftime('%d.%m'))

        return dates

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
            self._create_chat(), self.from_obj, self.make_message_text())

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


class LectureConfirmRespondentChatService(ChatService):
    response_message_text = f'Одна или более из выбранных вами дат на данную лекцию ' \
                            f'уже подтверждена для другого пользователя. ' \
                            f'Возможные даты проведения:'
    object_manager = ChatManager

    def __init__(self, from_obj: User, lecture_requests: QuerySet[LectureRequest],
                 respondent: Person, service):
        super().__init__(from_obj)
        self.lecture_requests = lecture_requests  # список подтвержденных дат лекции
        self.respondent = respondent
        self.service = service

    def format_dates_for_message(self, chat: Chat) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        dates = []
        for chat_request in self.object_manager.get_lecture_requests_by_chat(chat):
            dates.append(chat_request.event.datetime_start.strftime('%d.%m'))

        return dates

    def create_response_message(self, chat: Chat) -> None:
        message = self.object_manager.create_message(
            author=self.from_obj,
            chat=chat,
            text=self.make_message_text()
        )
        self.service.add_chat_message(message)

    def _handle_several_dates(self, chat: Chat, lecture_request: LectureRequest):
        """ Удаляет подтвержденную дату из всех чатов откликнувшихся на нее пользователей """

        self.object_manager.remove_lecture_request_from_chat(chat, lecture_request)
        self.create_response_message(chat)

    def _handle_single_date(self, chat: Chat):
        """ Удаляет чат """

        client = self.object_manager.get_user_from_chat(chat, self.from_obj)
        self.service.add_deleted_chat(DeletedChat(client=client, chat_id=chat.pk))
        self.object_manager.delete_chat(chat)

    def _handle_chats(self, chat_list: QuerySet[Chat], lecture_request: LectureRequest):
        for chat in chat_list:
            # Если в чате больше одной даты, то отправляем пользователю сообщение,
            # что какие-то из дат заняты
            if self.object_manager.count_chat_lecture_requests(chat) > 1:
                self._handle_several_dates(chat, lecture_request)
            else:
                # иначе удаляем чат и отправляем сообщение об удалении
                self._handle_single_date(chat)

    def _handle_lecture_requests(self) -> None:
        """ Обрабатывает чаты и все остальные отклики на подтвержденную лекцию:
        удаляет чат, если дата только одна,
        удаляет запрос на выбранную дату из списка запросов данного чата, если дат несколько """

        for lecture_request in self.lecture_requests:
            chat_list = self.object_manager.get_lecture_request_chats_with_exclude(
                lecture_request, self.respondent.user)

            self._handle_chats(chat_list, lecture_request)

    def setup(self):
        self._handle_lecture_requests()
