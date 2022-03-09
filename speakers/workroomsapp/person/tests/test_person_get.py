from django.urls import reverse
from rest_framework.test import APITestCase

from workroomsapp.models import City


class TestPersonGet(APITestCase):

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
        self.client.post(reverse('profile'), person_data)

    def test_credentials(self):
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('profile'))
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке получения профиля неавторизованного пользователя'
        )

    def test_person_get_successful(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(
            response.status_code, 200,
            msg='Неверный статус ответа при получении профиля пользователя'
        )

    def test_city_is_string(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(
            response.data['data'][0]['city'], 'Москва',
            msg='Неверное отображение города в ответе при получении профиля пользователя'
        )