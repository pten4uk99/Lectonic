import datetime

from django.urls import reverse
from rest_framework.test import APITestCase, override_settings

from authapp.models import User
from speakers.utils.tests import data
from speakers.utils.tests.upload_image import test_image
from workroomsapp.models import City, Person


@override_settings(MEDIA_URL=test_image.MEDIA_URL, MEDIA_ROOT=test_image.MEDIA_ROOT)
class TestPersonCreate(APITestCase):
    signup_data = data.SIGNUP.copy()
    profile_data = data.PROFILE.copy()
    profile_data['city'] = '1'

    def setUp(self):
        self.profile_data['photo'] = test_image.create_image()
        temp_data = self.signup_data.copy()
        self.client.post(reverse('signup'), temp_data)
        City.objects.create(name='Москва', pk=1)

    def test_person_was_created(self):
        temp_data = self.profile_data.copy()
        response = self.client.post(reverse('profile'), temp_data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании профиля пользователя'
        )

        user = User.objects.get(email=self.signup_data['email'])
        self.assertEqual(
            Person.objects.filter(user=user).exists(), True,
            msg='Профиль пользователя не был создан'
        )

    def test_person_created_twice(self):
        temp_data = self.profile_data.copy()
        self.client.post(reverse('profile'), temp_data)
        response = self.client.post(reverse('profile'), temp_data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при повторном создании профиля пользователя'
        )

    def test_person_city(self):
        temp_data = self.profile_data.copy()
        response = self.client.post(reverse('profile'), temp_data)
        self.assertEqual(
            response.data['data'][0]['city'], 'Москва',
            msg='Неверное отображение города в ответе при создании профиля пользователя'
        )

    def test_user_has_permissions(self):
        temp_data = self.profile_data.copy()
        self.client.get(reverse('logout'))
        response = self.client.post(reverse('profile'), temp_data)
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при создании профиля неавторизованного пользователя'
        )

    def test_required_fields_not_passed(self):
        temp_data = self.profile_data.copy()
        temp_data.pop('first_name')
        temp_data.pop('last_name')
        temp_data.pop('birth_date')
        temp_data.pop('city')

        response = self.client.post(reverse('profile'), temp_data)
        self.assertEqual(
            ('first_name' in response.data and
             'last_name' in response.data and
             'birth_date' in response.data and
             'city' in response.data and
             response.status_code == 400), True,
            msg='Неверный статус ответа при создании профиля пользователя с не переданными данными'
        )

    def test_name_validation(self):
        temp_data = self.profile_data.copy()
        temp_data['first_name'] = 'Petr'

        response = self.client.post(reverse('profile'), temp_data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при создании профиля пользователя с неверным форматом имени'
        )

    def test_birth_date_validation(self):
        temp_data = self.profile_data.copy()
        temp_data['birth_date'] = '202-01-18'

        response1 = self.client.post(reverse('profile'), temp_data)
        self.assertEqual(
            response1.status_code, 400,
            msg='Неверный статус ответа при создании профиля пользователя с неверным форматом даты рождения'
        )

        temp_data['birth_date'] = str(datetime.date.today() + datetime.timedelta(days=1))

        response2 = self.client.post(reverse('profile'), temp_data)
        self.assertEqual(
            response2.status_code, 400,
            msg='Неверный статус ответа при создании профиля пользователя датой рождения позже текущей'
        )