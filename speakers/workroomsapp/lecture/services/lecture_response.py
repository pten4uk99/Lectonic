import datetime

from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from chatapp.models import Message, Chat
from chatapp.services.chat import LectureCancelResponseChatService, LectureResponseChatService, \
    LectureConfirmRespondentChatService
from chatapp.services.ws import LectureCancelResponseWsService, LectureResponseWsService, \
    LectureConfirmRespondentWsService, DeletedChat
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.services.db import AttrNames, LectureResponseManager
from workroomsapp.lecture.services.service import LectureService
from workroomsapp.models import LectureRequest, Person


class LectureResponseBaseService(LectureService):
    object_manager = LectureResponseManager
    chat_service = None
    ws_service = None

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)

        # сообщает дополнительным сервисам необходимую информацию
        self.chat_service.setup()
        self.ws_service.setup()


class LectureResponseService(LectureResponseBaseService):
    chat_service = LectureResponseChatService
    ws_service = LectureResponseWsService

    def __init__(self, request: HttpRequest, from_obj: User,
                 lecture_id: int, response_dates: list[str],
                 from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj, lecture_id=lecture_id, from_attr=from_attr)
        self._lecture_creator = self._get_lecture_creator()
        self._responses = self._get_lecture_dates(response_dates)

        self.chat_service = self.chat_service(
            from_obj=from_obj, lecture=self.lecture,
            responses=self._responses, lecture_creator=self._lecture_creator)
        self.ws_service = self.ws_service(
            request, from_obj=from_obj, clients=[self._lecture_creator.user, self.from_obj],
            lecture_creator=self._lecture_creator, responses=self._responses)

    def _get_lecture_creator(self) -> Person:
        """ Возвращает объект Person создателя лекции. """

        creator = None

        if not self.lecture.customer:
            if not hasattr(self.from_obj.person, 'customer'):
                return lecture_responses.lecturer_forbidden()
        else:
            creator = self.lecture.customer.person

        if not self.lecture.lecturer:
            if not hasattr(self.from_obj.person, 'lecturer'):
                return lecture_responses.customer_forbidden()
        else:
            creator = self.lecture.lecturer.person

        return creator

    def _check_can_response(self):
        """ Проверяет, может ли пользователь откликнуться на текущую лекцию """

        lecture_requests = self.object_manager.get_person_rejected_lecture_requests(
            self.from_obj.person, self.lecture)
        if lecture_requests:
            return lecture_responses.can_not_response()

    def check_permissions(self, *args, **kwargs) -> bool:
        self._check_can_response()
        return super().check_permissions()

    # возможно форматирование дат стоит перенести куда-нибудь отдельно
    @staticmethod
    def _format_dates(dates: list[str]) -> list[datetime.datetime]:
        """ Форматирует переданные в запросе даты """

        format_dates = []

        for date in dates:
            format_dates.append(
                datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M'))

        return format_dates

    def _get_lecture_dates(self, dates: list[str]) -> QuerySet[LectureRequest]:
        """ Возвращает список LectureRequests по датам лекции """

        response_dates = self._format_dates(dates)
        return self.object_manager.get_responses(self.lecture, response_dates)

    def _add_respondent(self) -> None:
        """ Добавляет пользователя в откликнувшиеся на переданные даты лекции """

        self.object_manager.add_respondent(self.from_obj.person, self._responses)
        # logger.info(f'responses: {self._responses}')

    def to_do(self):
        self._add_respondent()  # пользователь добавляется в откликнувшиеся


class LectureCancelResponseService(LectureResponseBaseService):
    chat_service = LectureCancelResponseChatService
    ws_service = LectureCancelResponseWsService

    def __init__(self, request: HttpRequest, from_obj: User, lecture_id: int):
        super().__init__(from_obj, lecture_id)
        self._chat = self.object_manager.get_chat_from_lecture(self.lecture, self.from_obj)
        self.chat_id = self._chat.pk
        self.chat_service = self.chat_service(from_obj, chat=self._chat)
        self.ws_service = self.ws_service(
            request, from_obj, clients=self._chat.users.all(), chat_id=self.chat_id)

    # def _delete_wrong_chats(self):
    #     chats = Chat.objects.filter(lecture=self.get_lecture())
    #
    #     for elem in chats:
    #         if elem.users.all().count() < 2:
    #             elem.delete()
    #
    #     return lecture_responses.success_cancel([{'type': 'chat_does_not_exist'}])

    def _remove_respondent(self, lecture_request) -> None:
        """ Удаляет откликнувшегося у LectureRequest """

        respondent_obj = lecture_request.respondent_obj.filter(person=self.from_obj.person).first()

        if respondent_obj and not respondent_obj.rejected:
            lecture_request.respondents.remove(self.from_obj.person)
            lecture_request.save()

            # logger.info(f'respondent_obj: {respondent_obj}, rejected: {respondent_obj.rejected}')

    def remove_all_respondents(self) -> None:
        """ Удаляет всех откликнувшихся на лекцию """

        for lecture_request in self.lecture.lecture_requests.all():
            self._remove_respondent(lecture_request)

    def check_permissions(self):
        requests = self.lecture.lecture_requests.filter(respondents=self.from_obj.person)

        if not requests:
            return lecture_responses.can_not_cancel_response()

        return super().check_permissions()

    def to_do(self):
        self.remove_all_respondents()


class LectureConfirmRespondentService(LectureResponseBaseService):
    chat_service = LectureConfirmRespondentChatService
    ws_service = LectureConfirmRespondentWsService

    def __init__(self, request: HttpRequest, from_obj: User, lecture_id: int, respondent_id: int):
        super().__init__(from_obj, lecture_id)
        self._chat = self.object_manager.get_chat_from_lecture(self.lecture, self.from_obj)
        self.respondent = self.object_manager.get_person(respondent_id)

        confirmed_lectures = self.object_manager.get_confirmed_lecture_requests_in_chat(
            self.lecture, self._chat)
        self.chat_service = self.chat_service(from_obj, confirmed_lectures, self.respondent, self)

        self.chat_messages = []
        self.deleted_chats: list[DeletedChat] = []

        self.ws_service = self.ws_service(request, from_obj, self.chat_messages, self.deleted_chats)

    def add_chat_message(self, message: Message):
        """ Функция использующаяся как callback, передающаяся в chat_service, в котором
        при новом сообщении оно добавляется в self.chat_messages """

        self.chat_messages.append(message)

    def add_deleted_chat(self, deleted_chat: DeletedChat):
        """ Функция использующаяся как callback, передающаяся в chat_service, в котором при удалении
         чата, он добавляется в self.deleted_chats """

        self.deleted_chats.append(deleted_chat)

    def _check_is_possible(self) -> None:
        """ Проверяет не подтверждена ли уже лекция на даты в текущем чате """

        confirmed_lectures = self.object_manager.get_confirmed_lecture_requests_in_chat(
            self.lecture, self._chat)

        if confirmed_lectures:
            return lecture_responses.forbidden()

    def _remove_other_respondents(self, lecture_request: LectureRequest):
        """ Принимает запрос на лекцию и удаляет всех остальных откликнувшихся
         подтвержденной лекции """

        respondents = self.object_manager.get_lecture_request_respondents(lecture_request, self.respondent.pk)

        for respondent in respondents:
            self.object_manager.remove_lecture_request_respondent(lecture_request, respondent)

    def _confirm_respondent(self):
        """ Подтверждает откликнувшегося пользователя на выбранные даты
        и удаляет остальных откликнувшихся """

        for lecture_request in self.object_manager.get_lecture_requests_by_chat(self._chat):
            self._remove_other_respondents(lecture_request)
            self.object_manager.confirm_respondent(lecture_request, self.respondent)

    def check_permissions(self):
        self._check_is_possible()
        return super().check_permissions()

    def to_do(self):
        self._confirm_respondent()

    def get_message_data(self):
        data = super().get_message_data()
        data['confirm'] = True
        return data
