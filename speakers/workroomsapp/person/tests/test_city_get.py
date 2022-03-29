from django.urls import reverse
from rest_framework.test import APITestCase

from workroomsapp.models import City


class TestCityGet(APITestCase):

    def setUp(self):
        signup_data = {'email': 'admin@admin.ru', 'password': '12345678'}
        self.client.post(reverse('signup'), signup_data)
        City.objects.create(name='Москва', pk=1)
        City.objects.create(name='Ярославль', pk=2)
        City.objects.create(name='Ивантеевка', pk=3)
        City.objects.create(name='Щелково', pk=4)
        City.objects.create(name='Пушкино', pk=5)

    def test_credentials(self):
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('city'), {'name': 'Москва'})
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке получения города неавторизованного пользователя'
        )

    def test_filter_city(self):
        response1 = self.client.get(reverse('city'), {'name': 'О'})
        self.assertEqual(
            len(response1.data['data']), 4,
            msg='Неверно отфильтрованы города'
        )

        response2 = self.client.get(reverse('city'), {'name': 'пст'})
        self.assertEqual(
            response2.status_code, 224,
            msg='Неверный статус при получении пустого списка городов'
        )

    def test_no_data_passed(self):
        response = self.client.get(reverse('city'))
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при пустом теле запроса'
        )

