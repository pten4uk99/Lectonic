from django.urls import reverse

from workroomsapp.models import City
from workroomsapp.tests.base import SignUpTestCase


class TestCityGet(SignUpTestCase):
    def setUp(self):
        super().setUp()
        for index, name in enumerate(['Москва', 'Ярославль', 'Ивантеевка', 'Щелково', 'Пушкино']):
            City.objects.create(name=name, pk=index + 1)

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
            response2.status_code, 200,
            msg='Неверный статус при получении пустого списка городов'
        )

