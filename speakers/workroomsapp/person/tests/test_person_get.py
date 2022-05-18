from django.urls import reverse

from workroomsapp.person.tests.base import PersonCreateTestCase


class TestPersonGet(PersonCreateTestCase):
    def setUp(self):
        super().setUp()

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
            response.data['data'][0]['city']['name'], 'Москва',
            msg='Неверное отображение города в ответе при получении профиля пользователя'
        )