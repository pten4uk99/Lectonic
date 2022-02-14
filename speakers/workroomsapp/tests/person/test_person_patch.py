from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from workroomsapp.models import City, Person


class TestPersonPatch(APITestCase):

    def setUp(self):
        signup_data = {'email': 'admin@admin.ru', 'password': '12345678'}
        self.client.post(reverse('signup'), signup_data)

        person_data = {
            'first_name': 'Пётр-Петр',
            'last_name': 'Петр',
            'middle_name': 'Петрович',
            'birth_date': '2020-01-18',
            'city': '1',
            'description': 'Описанюшка',
        }

        City.objects.create(name='Москва', pk=1)
        City.objects.create(name='Ярославль', pk=2)
        self.client.post(reverse('profile'), person_data)

    def test_credentials(self):
        self.client.get(reverse('logout'))
        response = self.client.patch(reverse('profile'), {'city': '2'})
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке изменения профиля неавторизованного пользователя'
        )

    def test_person_successful_patched(self):
        data = {
            'first_name': 'Василий',
            'last_name': 'Головнов',
            'middle_name': 'Головиныч',
            'birth_date': '2018-01-18',
            'city': '2',
            'description': 'Новая описанюшка',
        }

        for key, value in data.items():
            response = self.client.patch(reverse('profile'), {key: value})
            self.assertEqual(
                response.status_code, 200,
                msg=f'Неверный статус ответа при изменении поля {key} профиля пользователя'
            )

            if key == 'city':
                self.assertEqual(
                    response.data['data'][0]['city'], 'Ярославль',
                    msg='Неверные данные в ответе при изменении города профиля пользователя'
                )

    def test_no_passed_data(self):
        response = self.client.patch(reverse('profile'))
        self.assertEqual(
            response.status_code, 400,
            msg=f'Не передано данных для изменения профиля пользователя'
        )

    def test_wrong_data(self):
        data = {
            'first_name': 'Василий1',
            'last_name': 'ГоловновD',
            'middle_name': 1,
            'birth_date': '201801-18',
            'city': 'Ярославль',
        }

        for key, value in data.items():
            response = self.client.patch(reverse('profile'), {key: value})
            self.assertEqual(
                response.status_code, 400,
                msg=f'Неверный статус ответа при неправильном изменении поля {key} профиля пользователя'
            )

        response = self.client.patch(reverse('profile'), {'city': '3'})
        self.assertEqual(
            response.status_code, 400,
            msg=f'Неверный статус ответа при неправильном изменении города профиля пользователя'
        )