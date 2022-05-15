from django.urls import reverse
from rest_framework.test import APITestCase, override_settings

from speakers.utils.tests import data
from speakers.utils.tests.upload_image import test_image
from workroomsapp.models import City


@override_settings(MEDIA_URL=test_image.MEDIA_URL, MEDIA_ROOT=test_image.MEDIA_ROOT)
class TestPersonGet(APITestCase):
    signup_data = data.SIGNUP.copy()
    profile_data = data.PROFILE.copy()
    profile_data['city'] = '1'

    def setUp(self):
        temp_signup_data = self.signup_data.copy()
        self.profile_data['photo'] = test_image.create_image()
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
            response.data['data'][0]['city'], 'Москва',
            msg='Неверное отображение города в ответе при получении профиля пользователя'
        )