import datetime

from django.db.models import QuerySet
from django.http import HttpRequest

from authapp.models import User
from services.base import LectureResponseBaseService, LectureService
from services.chat.lecture_response import LectureCancelResponseChatService, LectureResponseChatService, \
    LectureConfirmRespondentChatService, LectureRejectRespondentChatService
from services.db import DeleteLectureManager
from services.types import person_id_type, user_id_type
from workroomsapp.lecture import lecture_responses
from services.types import AttrNames
from workroomsapp.models import LectureRequest, Person


class LectureResponseService(LectureResponseBaseService):
    chat_service = LectureResponseChatService

    def __init__(self, from_obj: User, lecture_id: int, response_dates: list[str],
                 from_attr: AttrNames = AttrNames.LECTURER, ws_active: bool = True):
        super().__init__(from_obj, lecture_id=lecture_id, from_attr=from_attr)
        self._lecture_creator = self._get_lecture_creator()
        self._responses = self._get_lecture_dates(response_dates)

        self.chat_service = self.chat_service(
            from_obj=from_obj, lecture=self.lecture,
            responses=self._responses, lecture_creator=self._lecture_creator,
            ws_active=ws_active
        )

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

    def __init__(self, from_obj: User, lecture_id: int):
        super().__init__(from_obj, lecture_id)
        self._chat = self.object_manager.get_chat_from_lecture(self.lecture, self.from_obj)
        self.chat_id = self._chat.pk

        self.chat_service = self.chat_service(from_obj, chat=self._chat)

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
    """ Сервис, включающий логику по подтверждению откликнувшегося пользователя на лекцию """

    chat_service = LectureConfirmRespondentChatService

    def __init__(self, from_obj: User, chat_id: int, respondent_id: user_id_type):
        super().__init__(from_obj)
        self._chat = self.object_manager.get_chat(chat_id)
        self.lecture = self._chat.lecture
        self.respondent = self.object_manager.get_object_by_id(User, respondent_id).person

        confirmed_lectures = self.object_manager.get_confirmed_lecture_requests_in_chat(
            self.lecture, self._chat)
        self.chat_service = self.chat_service(
            from_obj, lecture_requests=confirmed_lectures,
            respondent=self.respondent, response_chat=self._chat)

    def _check_is_possible(self) -> None:
        """ Проверяет не подтверждена ли уже лекция на даты в текущем чате """

        confirmed_lectures = self.object_manager.get_confirmed_lecture_requests_in_chat(
            self.lecture, self._chat)

        if confirmed_lectures:
            return lecture_responses.forbidden()

    def _remove_other_respondents(self, lecture_request: LectureRequest) -> None:
        """ Принимает запрос на лекцию и удаляет всех остальных откликнувшихся
         подтвержденной лекции """

        respondents = self.object_manager.get_lecture_request_respondents(lecture_request, self.respondent.pk)

        for respondent in respondents:
            self.object_manager.remove_lecture_request_respondent(lecture_request, respondent)

    def _confirm_respondent(self) -> None:
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


class LectureRejectRespondentService(LectureResponseBaseService):
    """ Сервис, включающий логику по отклонению отклика пользователя на лекцию """

    chat_service = LectureRejectRespondentChatService

    def __init__(self, from_obj: User, chat_id: int, respondent_id: user_id_type):
        super().__init__(from_obj)
        self._chat = self.object_manager.get_chat(chat_id)
        self.lecture = self._chat.lecture
        self.respondent = self.object_manager.get_object_by_id(User, respondent_id).person

        self.chat_service = self.chat_service(
            from_obj, respondent=self.respondent, response_chat=self._chat)

    def _check_is_possible(self) -> None:
        """ Проверяет не подтверждена ли уже лекция на даты в текущем чате """

        rejected_lecture_requests = self.object_manager.get_person_rejected_lecture_requests(
            self.from_obj.person, self.lecture)

        if rejected_lecture_requests:
            return lecture_responses.forbidden()

    def _reject_respondent(self) -> None:
        """ Отклоняет откликнувшегося пользователя на выбранные им даты лекции """

        for lecture_request in self.object_manager.get_lecture_requests_by_chat(self._chat):
            self.object_manager.reject_respondent(lecture_request, self.respondent)

    def check_permissions(self):
        self._check_is_possible()
        return super().check_permissions()

    def to_do(self):
        self._reject_respondent()


class LectureDeleteService(LectureService):
    object_manager = DeleteLectureManager

    def check_permissions(self) -> bool:
        """ Проверяет является ли пользователь (self._from_obj), создателем лекции (lecture) """

        if self.lecture.lecturer:
            if not self.lecture.lecturer.person.user == self.from_obj:
                return lecture_responses.not_a_creator()
        elif self.lecture.customer:
            if not self.lecture.customer.person.user == self.from_obj:
                return lecture_responses.not_a_creator()

        return True

    def to_do(self) -> None:
        """ Удаляет объект Lecture из базы данных """

        self.object_manager.delete(self.lecture)
