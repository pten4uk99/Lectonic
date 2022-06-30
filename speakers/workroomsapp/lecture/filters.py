import datetime
from abc import ABC
from typing import Type, Union, Iterable

from workroomsapp.lecture.db import AttrNames, GetLectureManager
from workroomsapp.models import Lecture, Person, Customer, Lecturer


class BaseFilter:
    """ Базовый класс для фильтрации лекций """

    def __init__(self, person: Person, from_attr: AttrNames):
        self.person = person
        self.from_attr = from_attr
        self.to_attr = AttrNames.CUSTOMER if self.from_attr == AttrNames.LECTURER else AttrNames.LECTURER
        self._object_manager = GetLectureManager(person=person, from_attr=from_attr, to_attr=self.to_attr)

    def _generate_lecture_list(self, *args, **kwargs) -> Iterable[Lecture]:
        """ Базовый метод для формирования списка лекций """
        raise NotImplementedError()

    def filter(self, *args, **kwargs) -> Iterable[Lecture]:
        """ Базовый метод для реализации фильтрации """
        return self._generate_lecture_list(*args, **kwargs)


class CreatedLecturesFilter(BaseFilter, ABC):
    """ Класс для фильтрации собственных лекций пользователя """

    def _generate_lecture_list(self):
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

    # ПЕРЕНЕСТИ ИЗ SELF._OBJECT_MANAGER ВСЮ ЛОГИКУ И ОСТАВИТЬ ТАМ ТОЛЬКО ВЗАИМОДЕЙСТВИЕ С БД !!!!!!!!!!

    def _generate_lecture_list(self):
        """ Возвращает список собственных подтвержденных лекций +
        список подтвержденных лекций на которые пользователь отклинкнулся """
        # ПЕРЕНЕСТИ ИЗ SELF._OBJECT_MANAGER ВСЮ ЛОГИКУ И ОСТАВИТЬ ТАМ ТОЛЬКО ВЗАИМОДЕЙСТВИЕ С БД !!!!!!!!!!
        return (self._object_manager.get_person_confirmed_lectures() +
                self._object_manager.get_person_confirmed_responses())


class PotentialLecturesFilter(BaseFilter, ABC):
    """ Класс для фильтрации собственных лекций пользователя """

    @staticmethod
    def _get_attr_class(attr: AttrNames) \
            -> Union[Type[Lecturer], Type[Customer]]:

        if attr == AttrNames.LECTURER:
            return Lecturer
        elif attr == AttrNames.CUSTOMER:
            return Customer

    def _generate_lecture_list(self):
        attr_class = self._get_attr_class(self.to_attr)
        # берем все потенциальных создателей лекций
        creators = attr_class.objects.exclude(person=self.person)

        lectures = []

        for creator in creators:
            # проходимся по всем лекциям потенциального создателя
            for lecture in creator.lectures.all():
                lectures.append(lecture)

        return lectures

    def filter(self):
        lectures_list = super().filter()
        filtered_lectures = []

        for lecture in lectures_list:
            # если текущий пользователь уже подтвержден на лекцию,
            # переходим на следующую итерацию
            if self._object_manager.get_confirmed_lecture_request(lecture, self.person):
                continue

            latest_lecture_date = self._object_manager.get_latest_lecture_date(lecture)

            if latest_lecture_date > datetime.datetime.now():
                filtered_lectures.append(lecture)

        return filtered_lectures
