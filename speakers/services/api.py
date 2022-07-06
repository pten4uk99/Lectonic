from abc import ABC, abstractmethod
from typing import Type

from django.http import HttpRequest
from rest_framework.serializers import Serializer

from authapp.models import User
from chatapp.chatapp_serializers import MessageListSerializer
from services.chat.chatapp import ChatMessageService
from services.create_user import UserCreateService
from services.filters import CreatedLecturesFilter, ConfirmedLecturesFilter, BaseFilter, \
    PotentialLecturesFilter
from workroomsapp.lecture.lecture_serializers import LecturesGetSerializer
from services.lecture import LectureResponseService, LectureCancelResponseService, \
    LectureConfirmRespondentService, LectureRejectRespondentService, LectureDeleteService
from services.types import person_id, UserLogin
from services import AttrNames
from workroomsapp.models import Person


# Тут описаны методы взаимодействия с представлениями

class BaseLectureAPI:
    def __init__(self, request: HttpRequest, person: Person, from_attr: AttrNames):
        self.request = request
        self.person = person
        self.from_attr = from_attr
        self.to_attr = AttrNames.LECTURER if self.from_attr == AttrNames.CUSTOMER else AttrNames.CUSTOMER


class SerializerAPI(BaseLectureAPI):
    serializer_class: Type[Serializer]

    @abstractmethod
    def init_serializer(self) -> Serializer:
        """ Создает объект self.serializer_class """

    def serialize(self) -> Serializer:
        """ Метод, который должен возвращать объект сериализатора с готовыми данными """
        return self.init_serializer()


class FilterAPI(SerializerAPI):
    """ Занимается отображением отфильтрованных объектов из БД """

    filter_class: Type[BaseFilter]

    def __init__(self, request: HttpRequest, person: Person, from_attr: AttrNames):
        super().__init__(request, person, from_attr)
        self._filter = self.filter_class(person=person, from_attr=from_attr)

    def init_serializer(self):
        filtered_lectures = self._filter.filter()
        return self.serializer_class(
            filtered_lectures, many=True, context={'request': self.request, 'query_from': self.from_attr.value})


class LectureGetAPI(FilterAPI, ABC):
    """ API для работы с получением лекций """
    serializer_class = LecturesGetSerializer


class CreatedLecturesGetAPI(LectureGetAPI):
    """ API для обработки и сериализации созданных лекций пользователя """
    filter_class = CreatedLecturesFilter


class ConfirmedLecturesGetAPI(LectureGetAPI):
    """ API для обработки и сериализации подтвержденных лекций и подтвержденных откликов пользователя """
    filter_class = ConfirmedLecturesFilter


class PotentialLecturesGetAPI(LectureGetAPI):
    """ API для обработки и сериализации подтвержденных лекций и подтвержденных откликов пользователя """
    filter_class = PotentialLecturesFilter


class ChatMessageAPI(SerializerAPI):
    serializer_class = MessageListSerializer
    service = ChatMessageService

    def __init__(self, request: HttpRequest, from_obj: User,
                 chat_id: int, from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(request, person=from_obj.person, from_attr=from_attr)
        self.service = self.service(request, from_obj=from_obj, chat_id=chat_id, from_attr=from_attr)

    def init_serializer(self) -> Serializer:
        return self.serializer_class(
            self.service.chat_messages, many=True, context={'user': self.service.from_obj})

    def serialize(self) -> Serializer:
        self.service.setup()
        return super().serialize()


# ------------------Функции для использования непосредственно в представлениях-------------------
# ---------------------------------------------------------------------------------------
def serialize_created_lectures(request: HttpRequest, person: Person, from_attr: AttrNames):
    return CreatedLecturesGetAPI(request=request, person=person, from_attr=from_attr).serialize()


def serialize_confirmed_lectures(request: HttpRequest, person: Person, from_attr: AttrNames):
    return ConfirmedLecturesGetAPI(
        request=request,
        person=person,
        from_attr=from_attr,
    ).serialize()


def serialize_potential_lectures(request: HttpRequest, person: Person, from_attr: AttrNames):
    return PotentialLecturesGetAPI(
        request=request,
        person=person,
        from_attr=from_attr
    ).serialize()


def service_delete_lecture_by_id(user: User, lecture_id: int) -> None:
    service = LectureDeleteService(from_obj=user, lecture_id=lecture_id)
    service.setup()


def service_response_to_lecture(request: HttpRequest, lecture_id: int, dates: list[str], ws_active: bool = True):
    service = LectureResponseService(
        request, from_obj=request.user, lecture_id=lecture_id, response_dates=dates, ws_active=ws_active)
    service.setup()


def service_cancel_response_to_lecture(request: HttpRequest, lecture_id: int):
    service = LectureCancelResponseService(request=request, from_obj=request.user, lecture_id=lecture_id)
    service.setup()


def service_confirm_respondent_to_lecture(request: HttpRequest, chat_id: int, respondent_id: person_id):
    service = LectureConfirmRespondentService(
        request, from_obj=request.user, chat_id=chat_id, respondent_id=respondent_id)
    service.setup()


def service_reject_respondent_to_lecture(request: HttpRequest, chat_id: int, respondent_id: person_id):
    service = LectureRejectRespondentService(
        request, from_obj=request.user, chat_id=chat_id, respondent_id=respondent_id)
    service.setup()


def serialize_chat_message_list(request: HttpRequest, chat_id: int):
    return ChatMessageAPI(request, from_obj=request.user, chat_id=chat_id).serialize()


def user_signup_service(data: dict, pk: int = None) -> tuple[UserLogin, Serializer]:
    service = UserCreateService(data=data, pk=pk)
    return service.setup(), service.serializer
