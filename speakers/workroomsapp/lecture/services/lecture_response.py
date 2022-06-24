import datetime

from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from chatapp.models import Chat
from chatapp.services.chat import LectureCancelResponseChatService, LectureResponseChatService
from chatapp.services.ws import LectureCancelResponseWsService, LectureResponseWsService
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.services.db import LectureCancelResponseManager, AttrNames, LectureResponseManager
from workroomsapp.lecture.services.service import LectureService
from workroomsapp.models import LectureRequest, Person


class LectureResponseBaseService(LectureService):
    object_manager = None
    chat_service = None
    ws_service = None

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)

        # сообщает дополнительным сервисам необходимую информацию
        self.chat_service.setup()
        self.ws_service.setup()


class LectureResponseService(LectureResponseBaseService):
    object_manager = LectureResponseManager
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
    object_manager = LectureCancelResponseManager
    chat_service = LectureCancelResponseChatService
    ws_service = LectureCancelResponseWsService

    def __init__(self, request: HttpRequest, from_obj: User, lecture_id: int):
        super().__init__(from_obj, lecture_id)
        self._chat = self._get_chat()
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

    def _get_chat(self) -> Chat:
        chat = self.object_manager.get_chat_from_lecture(self.lecture, self.from_obj)
        return chat

    def _remove_respondent(self, lecture_request) -> None:
        """ Удаляет откликнувшегося у LectureRequest """

        respondent_obj = lecture_request.respondent_obj.filter(person=self.from_obj.person).first()

        if respondent_obj and not respondent_obj.rejected:
            lecture_request.respondents.remove(self.from_obj.person)
            lecture_request.save()

            # logger.info(f'respondent_obj: {respondent_obj}, rejected: {respondent_obj.rejected}')

    def remove_all_respondents(self):
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
