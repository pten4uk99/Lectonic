from django.db.models import QuerySet

from authapp.models import User
from chatapp.models import Chat, Message
from services.chat.base import ChatService, SystemMessageForRecipientText, SystemMessageForAuthorText, \
    CurrentChatMessagesChatService
from services.types import AttrNames
from services.ws.lecture_response import LectureResponseWsService, LectureCancelResponseWsService, \
    LectureConfirmRespondentWsService, LectureRejectRespondentWsService
from workroomsapp.models import Lecture, LectureRequest, Person
from django.db.models import QuerySet

from authapp.models import User
from chatapp.models import Chat
from services.chat.base import ChatService
from services.types import AttrNames
from services.ws.lecture_response import LectureResponseWsService, LectureCancelResponseWsService, \
    LectureConfirmRespondentWsService, LectureRejectRespondentWsService
from workroomsapp.models import Lecture, LectureRequest, Person


class LectureResponseChatService(CurrentChatMessagesChatService):
    message_for_author: SystemMessageForAuthorText = SystemMessageForAuthorText.lecture_response
    message_for_recipient: SystemMessageForRecipientText = SystemMessageForRecipientText.lecture_response
    ws_service = LectureResponseWsService

    def __init__(self, from_obj: User, lecture: Lecture,
                 responses: QuerySet[LectureRequest], lecture_creator: Person,
                 from_attr: AttrNames = AttrNames.LECTURER, ws_active: bool = True):
        super().__init__(from_obj, from_attr)
        self._lecture = lecture
        self._lecture_responses = responses
        self._lecture_creator = lecture_creator

        self.ws_service = self.ws_service(
            from_obj, clients=[self._lecture_creator.user, self.from_obj],
            lecture_creator=self._lecture_creator, responses=responses, ws_active=ws_active)

    def format_dates_for_message(self) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        dates = []

        for response in self._lecture_responses:
            dates.append(response.event.datetime_start.strftime('%d.%m'))

        return dates

    def _get_str_dates(self) -> str:
        dates = self.format_dates_for_message()
        return ", ".join(dates)

    def build_message_for_author(self):
        return self.message_for_author.value + ' ' + self._get_str_dates()

    def build_message_for_recipient(self):
        return self.message_for_recipient.value + ' ' + self._get_str_dates()

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

        return chat

    def to_do(self) -> None:
        """ Создает новый чат (если его до этого не существовало) и
        стандартное сообщение в чате при отклике """

        chat = self._create_chat()
        self.create_current_chat_messages(chat)


class LectureCancelResponseChatService(ChatService):
    ws_service = LectureCancelResponseWsService

    def __init__(self, from_obj: User, chat: Chat):
        super().__init__(from_obj)
        self._chat = chat

        clients = list(self._chat.users.all())
        self.ws_service = self.ws_service(from_obj, clients=clients, chat_id=self._chat.pk)

    def _remove_chat(self) -> None:
        self.object_manager.delete_chat(self._chat)

    def to_do(self):
        self._remove_chat()


class LectureConfirmRespondentChatService(CurrentChatMessagesChatService):
    message_for_author = SystemMessageForAuthorText.confirm_lecture
    message_for_recipient = SystemMessageForRecipientText.confirm_lecture
    other_respondents_message = f'Одна или более из выбранных вами дат на данную лекцию ' \
                                f'уже подтверждена для другого пользователя. ' \
                                f'Возможные даты проведения:'
    ws_service = LectureConfirmRespondentWsService

    def __init__(self, from_obj: User,
                 lecture_requests: QuerySet[LectureRequest],
                 respondent: Person, response_chat: Chat):
        super().__init__(from_obj)
        self.lecture_requests = lecture_requests  # список подтвержденных дат лекции
        self.respondent = respondent
        self.response_chat = response_chat

        self.ws_service = self.ws_service(from_obj, clients=self.response_chat.users.all())

    def format_dates_for_message(self, chat: Chat) -> list[str]:
        """ Приводит даты лекции к формату dd.mm и возвращает список отформатированных строк """

        dates = []
        for chat_request in self.object_manager.get_lecture_requests_by_chat(chat):
            dates.append(chat_request.event.datetime_start.strftime('%d.%m'))

        return dates

    def _build_message_for_other_respondent(self, chat: Chat) -> str:
        dates = self.format_dates_for_message(chat)
        str_dates = ", ".join(dates)
        return self.other_respondents_message + ' ' + str_dates

    def _create_message_for_other_respondent(self, chat: Chat) -> None:
        """ Создает сообщение для откликнувшегося на лекцию, которого не подтвердили """

        message = self.object_manager.create_message(
            author=self.from_obj,
            chat=chat,
            text=self._build_message_for_other_respondent(chat)
        )
        client = self.object_manager.get_user_from_chat(message.chat, exclude_user=self.from_obj)
        self.ws_service.send_message(message, client)

    def _handle_several_dates(self, chat: Chat, lecture_request: LectureRequest):
        """ Удаляет подтвержденную дату из всех чатов откликнувшихся на нее пользователей """

        self.object_manager.remove_lecture_request_from_chat(chat, lecture_request)
        self._create_message_for_other_respondent(chat)

    def _handle_single_date(self, chat: Chat):
        """ Удаляет чат и отправляет сообщение об удалении по вебсокету """

        client = self.object_manager.get_user_from_chat(chat, self.from_obj)
        self.ws_service.send_delete_chat_message_to_other_respondent(chat, client)
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

    def send_ws_message(self, message: Message, client: User):
        self.ws_service.send_message(message, client=client)

    def to_do(self):
        self.create_current_chat_messages(self.response_chat)
        self._handle_lecture_requests()


class LectureRejectRespondentChatService(CurrentChatMessagesChatService):
    """ Сервис, включающий логику по обработки отклонения откликнувшегося пользователя на лекцию """

    message_for_author = SystemMessageForAuthorText.reject_lecture
    message_for_recipient = SystemMessageForRecipientText.reject_lecture

    ws_service = LectureRejectRespondentWsService

    def __init__(self, from_obj: User, respondent: Person, response_chat: Chat):
        super().__init__(from_obj)
        self.respondent = respondent
        self.response_chat = response_chat

        self.ws_service = self.ws_service(from_obj, clients=[self.from_obj, self.respondent.user])

    def _reject_chat(self):
        """ Ставит чату пометку confirm=False """

        self.response_chat.confirm = False
        self.response_chat.save()

    def send_ws_message(self, message: Message, client: User):
        self.ws_service.send_message(message)

    def to_do(self):
        self.create_current_chat_messages(self.response_chat)
        self._reject_chat()
