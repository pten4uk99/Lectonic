from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import Token, User


class TestLogin(APITestCase):

    def setUp(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}
        User.objects.create(**data)

    def test_user_successful_authenticated(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}

        response = self.client.post(reverse('login'), data)
        self.assertEqual(
            response.status_code, 200,
            msg='Пользователь не был авторизован'
        )

        user = User.objects.get(email=data['email'])
        self.assertEqual(
            user.is_authenticated, True,
            msg='Пользователь не был авторизован'
        )
        self.assertEqual(
            Token.objects.filter(user=user).exists(), True,
            msg='Токен для пользователя не был создан в базе данных'
        )

    def test_twice_authentication(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}

        self.client.post(reverse('login'), data)
        response = self.client.post(reverse('login'), data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус кода при повторной авторизации пользователя'
        )

    def test_no_body_in_request(self):
        data = {'password': '12345678'}

        response1 = self.client.post(reverse('login'), data)
        self.assertEqual(
            response1.status_code, 400,
            msg='Неверный статус ответа при отсутствии эмейла в теле запроса'
        )

        data = {'email': 'admin@admin.ru'}

        response2 = self.client.post(reverse('login'), data)
        self.assertEqual(
            response2.status_code, 400,
            msg='Неверный статус ответа при отсутствии пароля в теле запроса'
        )

    def test_wrong_data(self):
        data = {'email': 'admin@admin.ru', 'password': '1234567'}

        response = self.client.post(reverse('login'), data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус кода при вводе неверного пароля'
        )

        data = {'email': 'admin@admin.ri', 'password': '12345678'}

        response = self.client.post(reverse('login'), data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус кода при вводе несуществующего эмейла'
        )

    def test_empty_body(self):
        response = self.client.post(reverse('login'), {})
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус кода при отправке запроса без тела'
        )
