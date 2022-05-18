from django.urls import reverse
from rest_framework.test import APITestCase

from speakers.utils.tests import data
from workroomsapp.models import City


class TestPersonGet(APITestCase):
    signup_data = data.SIGNUP.copy()
    profile_data = data.PROFILE.copy()
    profile_data['city'] = '1'

    def setUp(self):
        temp_signup_data = self.signup_data.copy()
        temp_profile_data = self.profile_data.copy()
        self.client.post(reverse('signup'), temp_signup_data)

        City.objects.create(name='Москва', pk=1)
        self.client.post(reverse('profile'), temp_profile_data)

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