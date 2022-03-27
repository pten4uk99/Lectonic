import datetime
import os

from django.urls import reverse

from rest_framework.test import APITestCase, override_settings

from authapp.models import User
from speakers.utils.tests import data
from speakers.utils.tests.upload_image import test_image
from workroomsapp.models import *


@override_settings(MEDIA_URL=test_image.MEDIA_URL, MEDIA_ROOT=test_image.MEDIA_ROOT)
class TestLectureAsLecturerCreate(APITestCase):
    signup_data = data.SIGNUP.copy()
    profile_data = data.PROFILE.copy()
    lecturer_data = data.LECTURER.copy()
    lecture_data = data.LECTURE.copy()

    def setUp(self):
        temp_data = self.lecture_data.copy()
        temp_data['photo'] = test_image.create_image()
        self.client.post(reverse('signup'), self.signup_data)
        user = User.objects.get(email=self.signup_data['email'])
        Person.objects.create(
            user=user,
            **self.profile_data,
            city=City.objects.create(name='Москова')
        )
        Domain.objects.create(pk=1, name='Канцелярия')
        Domain.objects.create(pk=2, name='Бухгалтерия')
        Domain.objects.create(pk=3, name='Юриспруденция')

        self.client.post(reverse('lecturer'), self.lecturer_data)
        temp_data = self.lecture_data.copy()
        temp_data['photo'] = test_image.create_image()
        self.client.post(reverse('lecture_as_lecturer'), temp_data)

    def test_success_response(self):
        lecture = Lecture.objects.first()
        response = self.client.get(reverse('lecture_response'), {'lecture': lecture.pk})
        self.assertEqual(
            response.status_code,
            200,
            msg='Неверный статус ответа при отклике на лекцию'
        )
        self.assertEqual(
            LectureRequest.objects.get(lecture=lecture).respondents.all().exists(),
            True,
            msg='Пользователь не добавился в откликнувшиеся на лекцию'
        )

    def test_success_confirm(self):
        lecture = Lecture.objects.first()
        response = self.client.get(reverse('lecture_confirm'), {'lecture': lecture.pk})
        self.assertEqual(
            response.status_code,
            200,
            msg='Неверный статус ответа при отклике на лекцию'
        )
        self.assertEqual(
            LectureRequest.objects.get(lecture=lecture).respondents.all().exists(),
            True,
            msg='Пользователь не добавился в откликнувшиеся на лекцию'
        )
