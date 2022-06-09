import datetime
from abc import ABC
from workroomsapp.lecture.services.db import AttrNames, GetLectureManager
from workroomsapp.models import Lecture, Person


class BaseFilter:
    """ Базовый класс для фильтрации лекций """

    def __init__(self, person: Person, from_attr: AttrNames, to_attr: AttrNames = None):
        self._object_manager = GetLectureManager(person=person, from_attr=from_attr, to_attr=to_attr)

    def generate_lecture_list(self, *args, **kwargs):
        """ Базовый метод для формирования списка лекций """
        raise NotImplementedError()

    def filter(self, *args, **kwargs):
        """ Базовый метод для реализации фильтрации """
        return self.generate_lecture_list(*args, **kwargs)


class CreatedLecturesFilter(BaseFilter, ABC):
    """ Класс для фильтрации собственных лекций пользователя """

    def generate_lecture_list(self):
        return self._object_manager.get_person_lectures()

    def filter(self) -> list[Lecture]:
        """ Фильтрует список лекций лектора по дате: возвращает все лекции,
        у которых хотя бы одна дата (самая поздняя) позже datetime.now() """

        lectures_list = super().filter()
        filtered_lectures = []

        for lecture in lectures_list:
            latest_lecture_date = self._object_manager.get_latest_lecture_date(lecture)

            if latest_lecture_date > datetime.datetime.now():
                filtered_lectures.append(lecture)

        return filtered_lectures


class ConfirmedLecturesFilter(BaseFilter, ABC):
    """ Класс для фильтрации собственных лекций пользователя """

    def generate_lecture_list(self):
        """ Возвращает список собственных подтвержденных лекций +
        список подтвержденных лекций на которые пользователь отклинкнулся """

        return (self._object_manager.get_person_confirmed_lectures() +
                self._object_manager.get_person_confirmed_responses())
