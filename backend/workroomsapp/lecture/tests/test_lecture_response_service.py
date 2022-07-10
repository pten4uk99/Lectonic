from django.http import HttpRequest
from rest_framework.test import APITestCase

from chatapp.models import Chat
from config.utils.tests import data
from services.api import service_response_to_lecture, service_cancel_response_to_lecture, \
    service_confirm_respondent_to_lecture, service_reject_respondent_to_lecture
from workroomsapp.models import *
from workroomsapp.person.tests.base import LecturerTestManager, CustomerTestManager, LectureTestManager


class LectureResponseTestCase(APITestCase):
    def setUp(self):
        self.lecturer_manager = LecturerTestManager()
        self.customer_manager = CustomerTestManager()

        self.lecturer_manager.create_obj()
        self.customer_manager.create_obj()

        lecture_manager = LectureTestManager(Lecturer.objects.first())
        lecture_manager.create_obj(2)

        lecture = Lecture.objects.first()

        self._user = self.customer_manager._user # откликается Customer
        service_response_to_lecture(
            self._user,
            lecture_id=lecture.pk,
            dates=[lecture.lecture_requests.first().event.datetime_start.strftime('%Y-%m-%dT%H:%M')])

    def test_response_on_lecture(self):
        self.assertEqual(
            Lecture.objects.first().lecture_requests.first().respondents.all().exists(),
            True,
            msg='Пользователь не был добавлен в откликнувшиеся на лекцию'
        )


class LectureCancelResponseTestCase(LectureResponseTestCase):
    def test_cancel_response_on_lecture(self):
        lecture_id = Lecture.objects.first().pk
        service_cancel_response_to_lecture(self._user, lecture_id)

        self.assertEqual(
            Lecture.objects.first().lecture_requests.first().respondents.all().exists(),
            False,
            msg='Пользователь не был удален из откликнувшихся на лекцию'
        )


class LectureConfirmRespondentTestCase(LectureResponseTestCase):
    def test_confirm_respondent_on_lecture(self):
        chat_id = Chat.objects.first().pk
        respondent_id = self.customer_manager._person.pk
        self._user = self.lecturer_manager._user
        service_confirm_respondent_to_lecture(self._user, chat_id, respondent_id)

        self.assertEqual(
            Lecture.objects.first().lecture_requests.filter(respondent_obj__confirmed=True).exists(),
            True,
            msg='Отклик пользователя не был подтвержден'
        )

    def test_remove_other_respondents(self):
        customer_manager = CustomerTestManager()
        customer_manager.signup_data = data.SIGNUP3.copy()
        customer_manager.create_obj()

        lecture = Lecture.objects.first()
        user = customer_manager._user

        service_response_to_lecture(
            user,
            lecture_id=lecture.pk,
            dates=[lecture.lecture_requests.first().event.datetime_start.strftime('%Y-%m-%dT%H:%M')]
        )

        chat = Chat.objects.first()
        respondent_id = self.customer_manager._person.pk
        service_confirm_respondent_to_lecture(self._user, chat.pk, respondent_id)
        self.assertEqual(
            lecture.lecture_requests.first().chat_list.all().count(), 1,
            msg='Чат не был удален'
        )


class LectureRejectRespondentTestCase(LectureResponseTestCase):
    def test_reject_respondent_on_lecture(self):
        chat_id = Chat.objects.first().pk
        respondent_id = self.customer_manager._person.pk
        self._user = self.lecturer_manager._user
        service_reject_respondent_to_lecture(self._user, chat_id, respondent_id)

        self.assertEqual(
            Lecture.objects.first().lecture_requests.filter(respondent_obj__rejected=True).exists(),
            True,
            msg='Отклик пользователя не был отклонен'
        )
