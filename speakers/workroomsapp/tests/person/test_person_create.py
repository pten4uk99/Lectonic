import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from workroomsapp.models import City, Person


class TestPersonCreate(APITestCase):

    def setUp(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}
        self.client.post(reverse('signup'), data)
        City.objects.create(name='Москва', pk=1)

    def test_person_was_created(self):
        data = {
            'first_name': 'Пётр-Петр',
            'last_name': 'Петр',
            'middle_name': 'Петрович',
            'birth_date': '2020-01-18',
            'city': '1',
            'description': 'Описанюшка',
        }

        response = self.client.post(reverse('profile'), data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании профиля пользователя'
        )

        user = User.objects.get(email='admin@admin.ru')
        self.assertEqual(
            Person.objects.filter(user=user).exists(), True,
            msg='Профиль пользователя не был создан'
        )

    def test_person_created_twice(self):
        data = {
            'first_name': 'Пётр-Петр',
            'last_name': 'Пётров-Петров',
            'middle_name': 'Пётров-Петров',
            'birth_date': '2020-01-18',
            'city': '1',
            'description': 'Описанюшка',
        }

        self.client.post(reverse('profile'), data)
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при повторном создании профиля пользователя'
        )

    def test_person_created_with_existing_data(self):
        profile_data = {
            'first_name': 'Пётр-Петр',
            'last_name': 'Пётров-Петров',
            'middle_name': 'Пётров-Петров',
            'birth_date': '2020-01-18',
            'city': '1',
            'description': 'Описанюшка',
        }

        self.client.post(reverse('profile'), profile_data)

        signup_data = {'email': 'admin@admin.com', 'password': '12345678'}
        self.client.post(reverse('signup'), signup_data)

        response = self.client.post(reverse('profile'), profile_data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании двух одинаковых профиля пользователей'
        )

    def test_person_city(self):
        profile_data = {
            'first_name': 'Пётр-Петр',
            'last_name': 'Пётров-Петров',
            'middle_name': 'Пётров-Петров',
            'birth_date': '2020-01-18',
            'city': '1',
            'description': 'Описанюшка',
        }

        response = self.client.post(reverse('profile'), profile_data)
        self.assertEqual(
            response.data['data'][0]['city'], 'Москва',
            msg='Неверное отображение города в ответе при создании профиля пользователя'
        )

    def test_user_has_permissions(self):
        data = {
            'first_name': 'Пётр-Петр',
            'last_name': 'Пётров-Петров',
            'middle_name': 'Пётров-Петров',
            'birth_date': '2020-01-18',
            'city': '1',
            'description': 'Описанюшка',
        }

        self.client.get(reverse('logout'))
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при создании профиля неавторизованного пользователя'
        )

    def test_required_fields_not_passed(self):
        data = {
            # 'first_name': 'Пётр-Петр',
            # 'last_name': 'Пётров-Петров',
            'middle_name': 'Пётров-Петров',
            # 'birth_date': '2020-01-18',
            # 'city': '1',
            'description': 'Описанюшка',
        }

        response = self.client.post(reverse('profile'), data)
        self.assertEqual(
            ('first_name' in response.data and
             'last_name' in response.data and
             'birth_date' in response.data and
             'city' in response.data and
             response.status_code == 400), True,
            msg='Неверный статус ответа при создании профиля пользователя с не переданными данными'
        )

    def test_name_validation(self):
        data = {
            'first_name': 'Petr',
            'last_name': 'Пётров-Петров',
            'middle_name': 'Пётров-Петров',
            'birth_date': '2020-01-18',
            'city': '1',
            'description': 'Описанюшка',
        }

        response = self.client.post(reverse('profile'), data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при создании профиля пользователя с неверным форматом имени'
        )

    def test_birth_date_validation(self):
        data = {
            'first_name': 'Пётр-Петр',
            'last_name': 'Пётров-Петров',
            'middle_name': 'Пётров-Петров',
            'birth_date': '202-01-18',
            'city': '1',
            'description': 'Описанюшка',
        }

        response1 = self.client.post(reverse('profile'), data)
        self.assertEqual(
            response1.status_code, 400,
            msg='Неверный статус ответа при создании профиля пользователя с неверным форматом даты рождения'
        )

        data['birth_date'] = str(datetime.date.today() + datetime.timedelta(days=1))

        response2 = self.client.post(reverse('profile'), data)
        self.assertEqual(
            response2.status_code, 400,
            msg='Неверный статус ответа при создании профиля пользователя датой рождения позже текущей'
        )