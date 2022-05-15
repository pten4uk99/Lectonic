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
    signup_data2 = data.SIGNUP2.copy()
    profile_data = data.PROFILE.copy()
    lecturer_data = data.LECTURER.copy()
    customer_data = data.CUSTOMER.copy()
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

        self.client.post(reverse('signup'), self.signup_data2)
        user = User.objects.get(email=self.signup_data2['email'])
        Person.objects.create(
            user=user,
            **self.profile_data,
            city=City.objects.create(name='Москова')
        )
        self.client.post(reverse('customer'), self.customer_data)

    def test_success_response(self):
        lecture = Lecture.objects.first()
        response = self.client.get(reverse('lecture_response'), {
            'lecture': lecture.pk,
            'date': (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        })

        self.assertEqual(
            response.status_code,
            200,
            msg='Неверный статус ответа при отклике на лекцию \n'
                f'Ответ: {response.data}'
        )
        self.assertEqual(
            LectureRequest.objects.get(lecture=lecture).respondents.all().exists(),
            True,
            msg='Пользователь не добавился в откликнувшиеся на лекцию'
        )

