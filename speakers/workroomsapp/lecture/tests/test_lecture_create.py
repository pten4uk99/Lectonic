import datetime
import os.path

from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from speakers.settings import BASE_DIR
from speakers.utils.tests import test_image
from workroomsapp.models import *


class TestLectureAsLecturerCreate(APITestCase):
    signup_data = {'email': 'admin@admin.ru', 'password': '12345678'}
    profile_data = {
        'first_name': 'Пётр-Петр',
        'last_name': 'Петр',
        'middle_name': 'Петрович',
        'birth_date': '2020-01-18',
        'description': 'Описанюшка',
    }
    lecturer_data = {
        'domain': ['1', '2', '3'],
        'performances_links': [
            'https://dev.lectonic.ru/city/?name=Москова',
            'http://dev.lectonic.com/com/com'
        ],
        'publication_links': [
            'https://dev.lectonic.ru/city/?name=Москова',
            'http://dev.lectonic.com/com/com'
        ],
        'education': 'У меня нереально высокое образование, я прям не могу',
        'hall_address': 'Москва, ул. Не московская, д. Домашний',
        'equipment': 'Руки, ноги, доска, полет.'
    }
    lecture_data = {
        'name': 'Лекция супер хорошая лекция',
        'datetime': '2020-03-15',
        'hall_address': 'Москва, ул. Не московская, д. Домашний',
        'type': 'offline',
        'equipment': 'Руки, ноги, доска, полет.',
        'duration': '30',
        'cost': '1000',
        'description': 'Отличное описание блин'
    }

    def setUp(self):
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
        with self.settings(
                MEDIA_URL='test_media',
                MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media')
        ):
            self.lecture_data['photo'] = test_image.start()
            response = self.client.post(reverse('lecture'), self.lecture_data)
            print(response.data)
            self.assertEqual(
                response.status_code, 201,
                msg='Неверный статус ответа при создании запроса на лекцию от лектора'
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
                LecturerLectureRequest.objects.all().exists(), True,
                msg='В базе не создан LecturerLectureRequest'
            )
        test_image.stop()

    def test_exist_lecture_request(self):
        self.client.post(reverse('lecture'), self.lecture_data)
        self.assertEqual(
            hasattr(Lecture.objects.first(), 'lecture_request'), True,
            msg='У созданной лекции нет аттрибута lecture_request'
        )

