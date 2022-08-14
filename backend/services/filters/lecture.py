from datetime import datetime

from django.db.models import QuerySet, Max, Q

from workroomsapp.models import Lecture
from .base import BaseFilter, FieldsFilter
from .fields import *

__all__ = [
    'LectureFilter',
    'FutureLectureFilter',
    'PermanentLectureFilter',
    'WithoutLecturersLectureFilter',
    'WithoutCustomersLectureFilter',
    'WithoutConfirmedLectureFilter',
    'WithoutCreatorLectureFilter',
    'WithoutPermanentLectureFilter',
    'PotentialLecturerLectureFilter',
    'PotentialCustomerLectureFilter',
    'ConfirmedCustomerLectureFilter',
    'ConfirmedLecturerLectureFilter',
    'CreatedCustomerLectureFilter',
    'CreatedLecturerLectureFilter',
]


class LectureFilter(BaseFilter):
    model = Lecture


class LectureFieldsFilter(FieldsFilter):
    model = Lecture


class PermanentLectureFilter(LectureFilter):
    """ Отфильтровывает только постоянные лекции """
    
    def _filter(self) -> QuerySet:
        qs = super()._filter()
        return qs.filter(lecture_requests=None)


class FutureLectureFilter(LectureFilter):
    def _filter(self) -> QuerySet[Lecture]:
        with_latest_date = self.qs.annotate(latest_date=Max('lecture_requests__event__datetime_start'))
        filtered_lectures = with_latest_date.filter(latest_date__gt=datetime.now())
        return filtered_lectures.distinct()


class WithoutPermanentLectureFilter(LectureFilter):
    """ Без постоянных лекций """
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        return qs.exclude(lecture_requests=None)


class WithoutConfirmedLectureFilter(LectureFilter):
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_confirmed_lectures = qs.exclude(lecture_requests__respondent_obj__confirmed=True)
        return without_confirmed_lectures.distinct()


class WithoutCreatorLectureFilter(LectureFilter):
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_creator = qs.exclude(
            Q(lecturer__person=self.from_obj.person) | Q(customer__person=self.from_obj.person))
        return without_creator.distinct()


class WithoutLecturersLectureFilter(LectureFilter):
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_lecturers = qs.filter(lecturer=None)
        return without_lecturers.distinct()


class WithoutCustomersLectureFilter(LectureFilter):
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_customers = qs.filter(customer=None)
        return without_customers.distinct()


# -------------------------------------------------------------------
# ------------------------Реализации---------------------------------
class PotentialLecturerLectureFilter(LectureFieldsFilter):
    fields = POTENTIAL_LECTURER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_lecturers = qs.filter(lecturer=None)
        return without_lecturers.distinct()


class PotentialCustomerLectureFilter(LectureFieldsFilter):
    fields = POTENTIAL_CUSTOMER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_customers = qs.filter(customer=None)
        return without_customers.distinct()


class ConfirmedLecturerLectureFilter(LectureFieldsFilter):
    fields = LECTURER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        
        # все лекции у которых либо создатель, либо откликнувшийся - текущий пользователь
        lectures_with_current_user = qs.filter(
            Q(lecturer__person__user=self.from_obj) | Q(lecture_requests__respondents__user=self.from_obj))
        
        # все подтвержденные лекции с текущим пользователем
        confirmed_lectures = lectures_with_current_user.filter(
            lecture_requests__respondent_obj__confirmed=True)
        
        return confirmed_lectures.distinct()


class ConfirmedCustomerLectureFilter(LectureFieldsFilter):
    fields = CUSTOMER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        
        # все лекции у которых либо создатель, либо откликнувшийся - текущий пользователь
        lectures_with_current_user = qs.filter(
            Q(customer__person__user=self.from_obj) | Q(lecture_requests__respondents__user=self.from_obj))
        
        # все подтвержденные лекции с текущим пользователем
        confirmed_lectures = lectures_with_current_user.filter(
            lecture_requests__respondent_obj__confirmed=True)
        
        return confirmed_lectures.distinct()


class CreatedLecturerLectureFilter(LectureFieldsFilter):
    fields = LECTURER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        return qs.filter(lecturer__person__user=self.from_obj)


class CreatedCustomerLectureFilter(LectureFieldsFilter):
    fields = CUSTOMER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        return qs.filter(customer__person__user=self.from_obj)
