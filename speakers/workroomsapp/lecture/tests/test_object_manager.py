import datetime
from datetime import timedelta
from typing import Union, Type
from unittest import TestCase

from django.db.models import QuerySet
from rest_framework.test import APITestCase

from workroomsapp.lecture.filters import AttrNames, GetLectureManager
from workroomsapp.models import Lecture, Lecturer, Customer
from workroomsapp.person.tests.base import LecturerTestManager, CustomerTestManager, LectureTestManager


class ObjectManagerTestCaseMixin:
    def _build(self, from_obj: Union[Type[Lecturer], Type[Customer]],
               to_obj: Union[Type[Lecturer], Type[Customer]]):
        l_manager = LecturerTestManager()
        c_manager = CustomerTestManager()
        l_manager.create_obj()
        c_manager.create_obj()

        lecture_manager = LectureTestManager(from_obj.objects.first())
        lecture_manager.create_obj(2)

        lecture = Lecture.objects.first()
        lecture_request = lecture.lecture_requests.first()
        lecture_request.respondents.add(to_obj.objects.first().person)
        lecture_request.save()
        respondent = lecture_request.respondent_obj.first()
        respondent.confirmed = True
        respondent.save()

    def _test_get_person_lectures(self: TestCase, from_obj, from_attr: AttrNames) -> None:
        manager = GetLectureManager(person=from_obj.objects.first().person, from_attr=from_attr)
        lectures = manager.get_person_lectures()
        self.assertEqual(
            isinstance(lectures, QuerySet), True,
            msg=f'{manager} неверно возвратил список лекций'
        )

    def _test_get_latest_lecture_date(self: TestCase, from_obj, from_attr: AttrNames) -> None:
        manager = GetLectureManager(person=from_obj.objects.first().person, from_attr=from_attr)
        latest_lecture_date = manager.get_latest_lecture_date(Lecture.objects.first())
        self.assertEqual(
            latest_lecture_date,
            datetime.datetime.now().replace(second=0, microsecond=0) + timedelta(days=3, hours=2),
            msg=f'{manager} неверно определил самую позднюю дату'
        )

    def _test_get_person_confirmed_lectures(self: TestCase, from_obj, from_attr: AttrNames):
        manager = GetLectureManager(person=from_obj.objects.first().person, from_attr=from_attr)
        confirmed_lectures = manager.get_person_confirmed_lectures()

        for lecture in confirmed_lectures:
            self.assertEqual(
                lecture.lecture_requests.filter(respondent_obj__confirmed=True).exists(),
                True,
                msg='Неверно отфильтрованы подтвержденные лекции'
            )

    def _test_get_person_confirmed_responses(self: TestCase, from_obj, from_attr: AttrNames):
        manager = GetLectureManager(person=from_obj.objects.first().person, from_attr=from_attr)
        confirmed_responses = manager.get_person_confirmed_responses()

        for lecture in confirmed_responses:
            self.assertEqual(
                lecture.lecture_requests.filter(respondent_obj__confirmed=True).exists(),
                True,
                msg='Неверно отфильтрованы подтвержденные отклики'
            )


class ObjectManagerForLecturerTestCase(APITestCase, ObjectManagerTestCaseMixin):
    def setUp(self):
        self._build(from_obj=Lecturer, to_obj=Customer)

    def test_get_lectures_from_person(self):
        self._test_get_person_lectures(Lecturer, AttrNames.LECTURER)

    def test_get_latest_lecture_date(self):
        self._test_get_latest_lecture_date(Lecturer, AttrNames.LECTURER)

    def test_get_person_confirmed_lectures(self):
        self._test_get_person_confirmed_lectures(Lecturer, AttrNames.LECTURER)

    def test_get_person_confirmed_responses(self):
        self._test_get_person_confirmed_responses(Customer, AttrNames.LECTURER)


class ObjectManagerForCustomerTestCase(APITestCase, ObjectManagerTestCaseMixin):
    def setUp(self):
        self._build(from_obj=Customer, to_obj=Lecturer)

    def test_get_lectures_from_person(self):
        self._test_get_person_lectures(Customer, AttrNames.CUSTOMER)

    def test_get_latest_lecture_date(self):
        self._test_get_latest_lecture_date(Customer, AttrNames.CUSTOMER)

    def test_get_person_confirmed_lectures(self):
        self._test_get_person_confirmed_lectures(Customer, AttrNames.CUSTOMER)

    def test_get_person_confirmed_responses(self):
        self._test_get_person_confirmed_responses(Lecturer, AttrNames.CUSTOMER)
