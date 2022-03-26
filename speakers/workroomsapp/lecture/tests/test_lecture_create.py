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

    def test_lecture_as_lecturer_was_created(self):
        temp_data = self.lecture_data.copy()
        temp_data['photo'] = test_image.create_image()
        response = self.client.post(reverse('lecture_as_lecturer'), temp_data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании запроса на лекцию от лектора\n'
                f'Ответ: {response.data}'
        )

        self.assertEqual(
            LectureRequest.objects.all().exists(), True,
            msg='В базе не создан LectureRequest'
        )
        self.assertEqual(
            Lecture.objects.all().exists(), True,
            msg='В базе не создан Lecture'
        )
        self.assertEqual(
            Optional.objects.all().exists(), True,
            msg='В базе не создан Optional'
        )
        self.assertEqual(
            Event.objects.all().exists(), True,
            msg='В базе не создан Event'
        )
        self.assertEqual(
            Calendar.objects.all().exists(), True,
            msg='В базе не создан Calendar'
        )
        self.assertEqual(
            LecturerCalendar.objects.all().exists(), True,
            msg='В базе не создан LecturerCalendar'
        )
        self.assertEqual(
            LectureDomain.objects.all().exists(), True,
            msg='В базе не создан LectureDomain'
        )
        self.assertEqual(
            LecturerLectureRequest.objects.all().exists(), True,
            msg='В базе не создан LecturerLectureRequest'
        )
        self.assertEqual(
            hasattr(Lecture.objects.first(), 'lecture_request'), True,
            msg='У созданной лекции нет аттрибута lecture_request'
        )
        self.assertEqual(
            os.path.exists(Lecture.objects.first().lecture_request.lecturer_lecture_request.photo.path),
            True,
            msg='Неверный путь изображения лекции'
        )

    def test_with_existing_datetime(self):
        temp_data = self.lecture_data.copy()
        temp_data['photo'] = test_image.create_image()
        self.client.post(reverse('lecture_as_lecturer'), temp_data)

        temp_data['photo'] = test_image.create_image()
        response2 = self.client.post(reverse('lecture_as_lecturer'), temp_data)
        self.assertEqual(
            response2.status_code,
            400,
            msg='Неверный статус ответа при создании события на существующую дату\n'
                f'Ответ: {response2.data}'
        )

        temp_data['photo'] = test_image.create_image()
        temp_data['time_start'] = '15:40'
        temp_data['time_end'] = '16:40'
        response3 = self.client.post(reverse('lecture_as_lecturer'), temp_data)
        self.assertEqual(
            response3.status_code,
            400,
            msg='Неверный статус ответа при создании события на существующую дату\n'
                f'Ответ: {response3.data}'
        )

        temp_data['photo'] = test_image.create_image()
        temp_data['time_start'] = '16:00'
        temp_data['time_end'] = '17:00'
        response4 = self.client.post(reverse('lecture_as_lecturer'), temp_data)
        self.assertEqual(
            response4.status_code,
            201,
            msg='Неверный статус ответа при создании события на не существующую дату\n'
                f'Ответ: {response4.data}'
        )

        temp_data['photo'] = test_image.create_image()
        temp_data['time_start'] = '15:15'
        temp_data['time_end'] = '15:30'
        response5 = self.client.post(reverse('lecture_as_lecturer'), temp_data)
        self.assertEqual(
            response5.status_code,
            201,
            msg='Неверный статус ответа при создании события на не существующую дату\n'
                f'Ответ: {response5.data}'
        )

        temp_data['photo'] = test_image.create_image()
        temp_data['time_start'] = '15:15'
        temp_data['time_end'] = '15:45'
        response5 = self.client.post(reverse('lecture_as_lecturer'), temp_data)
        self.assertEqual(
            response5.status_code,
            400,
            msg='Неверный статус ответа при создании события на существующую дату\n'
                f'Ответ: {response5.data}'
        )

