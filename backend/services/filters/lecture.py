from datetime import datetime

from django.db.models import QuerySet, Max, Q

from workroomsapp.models import Lecture
from .base import BaseFilter
from .fields import *

__all__ = [
    'LectureFilter',
    'FutureLectureFilter',
    'PotentialLectureFilter',
    'PotentialLecturerLectureFilter',
    'PotentialCustomerLectureFilter',
    'ConfirmedCustomerLectureFilter',
    'ConfirmedLecturerLectureFilter',
    'CreatedCustomerLectureFilter',
    'CreatedLecturerLectureFilter',
]


class LectureFilter(BaseFilter):
    model = Lecture


class FutureLectureFilter(LectureFilter):
    def _filter(self) -> QuerySet[Lecture]:
        with_latest_date = self.qs.annotate(latest_date=Max('lecture_requests__event__datetime_start'))
        filtered_lectures = with_latest_date.filter(latest_date__gt=datetime.now())
        return filtered_lectures.distinct()


class PotentialLectureFilter(FutureLectureFilter):
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_confirmed_lectures = qs.exclude(lecture_requests__respondent_obj__confirmed=True)
        without_creator = without_confirmed_lectures.exclude(
            Q(lecturer__person=self.from_obj.person) | Q(customer__person=self.from_obj.person))
        
        return without_creator.distinct()


# -------------------------------------------------------------------
# ------------------------Реализации---------------------------------
class PotentialLecturerLectureFilter(PotentialLectureFilter):
    fields = POTENTIAL_LECTURER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_lecturers = qs.filter(lecturer=None)
        return without_lecturers.distinct()


class PotentialCustomerLectureFilter(PotentialLectureFilter):
    fields = POTENTIAL_CUSTOMER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        without_customers = qs.filter(customer=None)
        return without_customers.distinct()


class ConfirmedLecturerLectureFilter(FutureLectureFilter):
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


class ConfirmedCustomerLectureFilter(FutureLectureFilter):
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


class CreatedLecturerLectureFilter(FutureLectureFilter):
    fields = LECTURER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        return qs.filter(lecturer__person__user=self.from_obj)


class CreatedCustomerLectureFilter(FutureLectureFilter):
    fields = CUSTOMER_LECTURE_FILTER_FIELDS
    
    def _filter(self) -> QuerySet[Lecture]:
        qs = super()._filter()
        return qs.filter(customer__person__user=self.from_obj)
