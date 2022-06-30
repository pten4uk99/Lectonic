from abc import ABC
from typing import Type

from django.http import HttpRequest
from rest_framework.serializers import Serializer

from authapp.models import User
from workroomsapp.lecture.db import AttrNames
from workroomsapp.lecture.filters import CreatedLecturesFilter, ConfirmedLecturesFilter, BaseFilter, \
    PotentialLecturesFilter
from workroomsapp.lecture.serializers.as_lecturer_serializers import LecturesGetSerializer
from workroomsapp.lecture.services.lecture_response import LectureResponseService, LectureCancelResponseService, \
    LectureConfirmRespondentService, LectureRejectRespondentService
from workroomsapp.lecture.services.service import LectureDeleteService
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

    def serialize(self) -> Serializer:
        """ Метод, который должен возвращать объект сериализатора с готовыми данными """

        raise NotImplementedError()


class FilterAPI(SerializerAPI):
    """ Занимается отображением отфильтрованных объектов из БД """

    filter_class: Type[BaseFilter]

    def __init__(self, request: HttpRequest, person: Person, from_attr: AttrNames):
        super().__init__(request, person, from_attr)
        self._filter = self.filter_class(person=person, from_attr=from_attr)

    def serialize(self) -> Serializer:
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


def service_response_to_lecture(request: HttpRequest, lecture_id: int, dates: list[str]):
    service = LectureResponseService(
        request, from_obj=request.user, lecture_id=lecture_id, response_dates=dates)
    service.setup()


def service_cancel_response_to_lecture(request: HttpRequest, lecture_id: int):
    service = LectureCancelResponseService(request=request, from_obj=request.user, lecture_id=lecture_id)
    service.setup()


def service_confirm_respondent_to_lecture(request: HttpRequest, lecture_id: int, respondent_id: int):
    service = LectureConfirmRespondentService(request, request.user, lecture_id, respondent_id)
    service.setup()


def service_reject_respondent_to_lecture(request: HttpRequest, lecture_id: int, respondent_id: int):
    service = LectureRejectRespondentService(request, request.user, lecture_id, respondent_id)
    service.setup()
