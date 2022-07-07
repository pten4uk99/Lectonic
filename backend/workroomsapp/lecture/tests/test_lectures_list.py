from django.http import HttpRequest
from rest_framework.test import APITestCase

from services.api import serialize_confirmed_lectures, serialize_potential_lectures
from services import AttrNames
from workroomsapp.models import Lecturer, Lecture, Customer
from workroomsapp.person.tests.base import LecturerTestManager, CustomerTestManager, LectureTestManager


class LecturesListTestCase(APITestCase):
    def setUp(self):
        l_manager = LecturerTestManager()
        c_manager = CustomerTestManager()
        l_manager.create_obj()
        c_manager.create_obj()

        l_lecture_manager = LectureTestManager(Lecturer.objects.first())
        c_lecture_manager = LectureTestManager(Customer.objects.first())
        l_lecture_manager.create_obj(2)
        c_lecture_manager.create_obj(1)

        lecture = Lecture.objects.first()
        lecture_request = lecture.lecture_requests.first()
        lecture_request.respondents.add(Customer.objects.first().person)
        lecture_request.save()
        respondent = lecture_request.respondent_obj.first()
        respondent.confirmed = True
        respondent.save()

        self._request = HttpRequest()

    def test_get_confirmed_lectures(self):
        self._request.user = Customer.objects.first().person.user

        serializer = serialize_confirmed_lectures(
            self._request, self._request.user.person,
            from_attr=AttrNames.CUSTOMER)

        self.assertEqual(
            len(serializer.data), 1,
            msg="Неверное количество подтвержденных лекций"
        )

    def test_get_potential_lectures(self):
        self._request.user = Customer.objects.first().person.user

        serializer = serialize_potential_lectures(
            self._request, self._request.user.person, from_attr=AttrNames.CUSTOMER)

        self.assertEqual(
            len(serializer.data), 1,
            msg="Неверное количество потенциальных лекций"
        )
