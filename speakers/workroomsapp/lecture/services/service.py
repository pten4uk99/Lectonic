from typing import Optional

from django.db.models import QuerySet

from authapp.models import User
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.services.db import DeleteLectureManager
from workroomsapp.models import Lecture


class Service:
    def __init__(self, from_obj: User):
        self._from_obj = from_obj

    def _check_permissions(self, *args, **kwargs) -> bool:
        """ Проверяет права """
        return True

    def to_do(self, *args, **kwargs) -> None:
        """ Метод, который вызывается снаружи класса, чтобы он выполнил свою работу """

        self._check_permissions()


class LectureDeleteService(Service):
    def __init__(self, from_obj: User, lecture_id: int):
        super().__init__(from_obj=from_obj)
        self._manager = DeleteLectureManager()
        self._lecture = self._manager.get_lecture_by_id(int(lecture_id))

    def _check_permissions(self) -> bool:
        """ Проверяет является ли пользователь (self._from_obj), создателем лекции (lecture) """

        if self._lecture.lecturer:
            if not self._lecture.lecturer.person.user == self._from_obj:
                return lecture_responses.not_a_creator()
        elif self._lecture.customer:
            if not self._lecture.customer.person.user == self._from_obj:
                return lecture_responses.not_a_creator()

        return True

    def to_do(self) -> None:
        """ Удаляет объект Lecture из базы данных """

        super().to_do()
        self._manager.delete(self._lecture)

