from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import Token, User


class TestLogout(APITestCase):

    def setUp(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}
        self.client.post(reverse('signup'), data)

    def test_user_successful_logged_out(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(
            response.status_code, 200,
            msg='Неверный статус ответа при попытке выхода пользователя из системы'
        )

        self.assertEqual(
            User.objects.get(email='admin@admin.ru').is_authenticated, False,
            msg='При выходе из системы флаг is_authenticated не установился в False'
        )

    def test_logged_out_twice(self):
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('logout'))
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке повторного выхода пользователя из системы'
        )

    def test_token_was_deleted(self):
        user = User.objects.get(email='admin@admin.ru')

        self.client.get(reverse('logout'))
        self.assertEqual(
            Token.objects.filter(user=user).exists(), False,
            msg='Токен не удалился при выходе из системы'
        )
