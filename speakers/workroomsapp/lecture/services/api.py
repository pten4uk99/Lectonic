from abc import ABC
from typing import Type

from rest_framework.request import Request
from rest_framework.serializers import Serializer

from authapp.models import User
from workroomsapp.lecture.serializers.as_lecturer_serializers import LecturesGetSerializer
from workroomsapp.lecture.services.db import AttrNames
from workroomsapp.lecture.services.filters import CreatedLecturesFilter, ConfirmedLecturesFilter, BaseFilter
from workroomsapp.lecture.services.service import Service, LectureDeleteService
from workroomsapp.models import Person


# Тут описаны методы взаимодействия с представлениями

class BaseAPI:
    def __init__(self, request: Request, person: Person, from_attr: AttrNames, to_attr: AttrNames = None):
        self.request = request
        self.person = person
        self.from_attr = from_attr
        self.to_attr = to_attr


class SerializerAPI(BaseAPI):
    serializer_class: Type[Serializer]

    def serialize(self) -> Serializer:
        """ Метод, который должен возвращать объект сериализатора с готовыми данными """

        raise NotImplementedError()


class FilterAPI(SerializerAPI):
    """ Занимается отображением отфильтрованных объектов из БД """

    filter_class: Type[BaseFilter]

    def __init__(self, request: Request, person: Person, from_attr: AttrNames, to_attr: AttrNames = None):
        super().__init__(request, person, from_attr, to_attr)
        self._filter = self.filter_class(person=person, from_attr=from_attr, to_attr=to_attr)

    def serialize(self) -> Serializer:
        filtered_lectures = self._filter.filter()
        return self.serializer_class(filtered_lectures, many=True, context={'request': self.request})


class LectureGetAPI(FilterAPI, ABC):
    """ API для работы с получением лекций """
    serializer_class = LecturesGetSerializer


class CreatedLecturesGetAPI(LectureGetAPI):
    """ API для обработки и сериализации созданных лекций пользователя """
    filter_class = CreatedLecturesFilter


class ConfirmedLecturesGetAPI(LectureGetAPI):
    """ API для обработки и сериализации подтвержденных лекций и подтвержденных откликов пользователя """
    filter_class = ConfirmedLecturesFilter


# ------------------Функции для использования непосредственно в представлениях-------------------
# ---------------------------------------------------------------------------------------
def serialize_created_lectures(request: Request, person: Person, from_attr: AttrNames):
    return CreatedLecturesGetAPI(request=request, person=person, from_attr=from_attr).serialize()


def serialize_confirmed_lectures(request: Request, person: Person, from_attr: AttrNames, to_attr: AttrNames):
    return ConfirmedLecturesGetAPI(
        request=request,
        person=person,
        from_attr=from_attr,
        to_attr=to_attr
    ).serialize()


def service_delete_lecture_by_id(user: User, lecture_id: int) -> None:
    service = LectureDeleteService(from_obj=user, lecture_id=lecture_id)
    service.to_do()
