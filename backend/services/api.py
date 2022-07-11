from abc import ABC, abstractmethod
from typing import Type, Iterable

from django.http import HttpRequest
from rest_framework.serializers import Serializer

from authapp.models import User
from chatapp.chatapp_serializers import ChatMessageListSerializer
from services.chat.chatapp import ChatMessageService
from services.authapp import UserCreateService
from services.filters import CreatedLecturesFilter, ConfirmedLecturesFilter, BaseFilter, \
    PotentialLecturesFilter
from workroomsapp.lecture.lecture_serializers import LecturesGetSerializer
from services.lecture import LectureResponseService, LectureCancelResponseService, \
    LectureConfirmRespondentService, LectureRejectRespondentService, LectureDeleteService
from services.types import person_id_type, UserLogin
from services import AttrNames
from workroomsapp.models import Person, Lecture


# Тут описаны методы взаимодействия с представлениями

class BaseLectureAPI:
    def __init__(self, from_obj: User, from_attr: AttrNames):
        self.from_obj = from_obj
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

    def __init__(self, from_obj: User, from_attr: AttrNames):
        super().__init__(from_obj, from_attr)
        self._filter = self.filter_class(from_obj=from_obj, from_attr=from_attr)

    def get_filtered_lectures(self) -> Iterable[Lecture]:
        return self._filter.filter()

    def init_serializer(self):
        return self.serializer_class(
            self.get_filtered_lectures(),
            many=True,
            context={'user': self.from_obj, 'query_from': self.from_attr.value}
        )


class LectureGetAPI(FilterAPI, ABC):
    """ API для работы с получением лекций """
    serializer_class = LecturesGetSerializer


class CreatedLecturesGetAPI(LectureGetAPI):
    """ API для обработки и сериализации созданных лекций пользователя """
    filter_class = CreatedLecturesFilter

    def init_serializer(self):
        return self.serializer_class(
            self.get_filtered_lectures(),
            many=True,
            context={'user': self.from_obj}
        )


class ConfirmedLecturesGetAPI(LectureGetAPI):
    """ API для обработки и сериализации подтвержденных лекций и подтвержденных откликов пользователя """
    filter_class = ConfirmedLecturesFilter


class PotentialLecturesGetAPI(LectureGetAPI):
    """ API для обработки и сериализации подтвержденных лекций и подтвержденных откликов пользователя """
    filter_class = PotentialLecturesFilter


class ChatMessageAPI(SerializerAPI):
    serializer_class = ChatMessageListSerializer
    service = ChatMessageService

    def __init__(self, from_obj: User, chat_id: int, from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj=from_obj, from_attr=from_attr)
        self.service = self.service(from_obj=from_obj, chat_id=chat_id, from_attr=from_attr)

    def init_serializer(self) -> Serializer:
        return self.serializer_class(
            [self.service.chat], many=True, context={'user': self.service.from_obj})

    def serialize(self) -> Serializer:
        self.service.setup()
        return super().serialize()


# ------------------Функции для использования непосредственно в представлениях-------------------
# ---------------------------------------------------------------------------------------
def serialize_created_lectures(from_obj: User, from_attr: AttrNames):
    return CreatedLecturesGetAPI(from_obj=from_obj, from_attr=from_attr).serialize()


def serialize_confirmed_lectures(from_obj: User, from_attr: AttrNames):
    return ConfirmedLecturesGetAPI(from_obj=from_obj, from_attr=from_attr).serialize()


def serialize_potential_lectures(from_obj: User, from_attr: AttrNames):
    return PotentialLecturesGetAPI(from_obj=from_obj, from_attr=from_attr).serialize()


def service_delete_lecture_by_id(from_obj: User, lecture_id: int) -> None:
    service = LectureDeleteService(from_obj=from_obj, lecture_id=lecture_id)
    service.setup()


def service_response_to_lecture(from_obj: User, lecture_id: int, dates: list[str], ws_active: bool = True):
    service = LectureResponseService(
        from_obj=from_obj, lecture_id=lecture_id, response_dates=dates, ws_active=ws_active)
    service.setup()


def service_cancel_response_to_lecture(from_obj: User, lecture_id: int):
    service = LectureCancelResponseService(from_obj=from_obj, lecture_id=lecture_id)
    service.setup()


def service_confirm_respondent_to_lecture(from_obj: User, chat_id: int, respondent_id: person_id_type):
    service = LectureConfirmRespondentService(from_obj=from_obj, chat_id=chat_id, respondent_id=respondent_id)
    service.setup()


def service_reject_respondent_to_lecture(from_obj: User, chat_id: int, respondent_id: person_id_type):
    service = LectureRejectRespondentService(from_obj=from_obj, chat_id=chat_id, respondent_id=respondent_id)
    service.setup()


def serialize_chat_message_list(from_obj: User, chat_id: int):
    return ChatMessageAPI(from_obj=from_obj, chat_id=chat_id).serialize()


def user_signup_service(data: dict, pk: int = None) -> tuple[UserLogin, Serializer]:
    service = UserCreateService(data=data, pk=pk)
    return service.setup(), service.serializer
