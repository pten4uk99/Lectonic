from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from authapp.models import Token


class TestSignup(APITestCase):
    def test_user_was_created(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}

        self.client.post(reverse('signup'), data)
        self.assertEqual(
            User.objects.filter(email=data['email']).exists(), True,
            msg='Пользователь не был создан в базе данных'
        )

    def test_password_was_hashed(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}

        self.client.post(reverse('signup'), data)
        self.assertEqual(
            User.objects.get(email=data['email']).check_password(data['password']),
            True,
            msg='Пароль неверно захешировался'
        )

    def test_user_successful_authenticated(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}

        self.client.post(reverse('signup'), data)
        user = User.objects.get(email=data['email'])
        self.assertEqual(
            user.is_authenticated, True,
            msg='Пользователь не был авторизован'
        )
        self.assertEqual(
            Token.objects.filter(user=user).exists(), True,
            msg='Токен для пользователя не был создан в базе данных'
        )

    def test_signup_twice(self):
        data = {'email': 'admin@admin.ru', 'password': '12345678'}

        self.client.post(reverse('signup'), data)
        response2 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response2.status_code, 400,
            msg='Неверный статус ответа при повторном создании пользователя'
        )

    def test_wrong_email(self):
        data = {'email': 'admin@admin.r', 'password': '12345678'}

        response1 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response1.status_code, 400,
            msg='Неверный статус ответа при вводе эмейла с одной буквой после точки'
        )

        data['email'] = 'admin@admin..ru'

        response2 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response2.status_code, 400,
            msg='Неверный статус ответа при вводе эмейла с двумя точками'
        )

        data['email'] = 'admin@@admin.ru'

        response3 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response3.status_code, 400,
            msg='Неверный статус ответа при вводе эмейла с двумя собаками'
        )

        data['email'] = 'admдin@admin.ru'

        response4 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response4.status_code, 400,
            msg='Неверный статус ответа при наличии русских символов в эмейле'
        )

        data['email'] = 'admin@adдmin.ru'

        response5 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response5.status_code, 400,
            msg='Неверный статус ответа при наличии русских символов в эмейле'
        )

        data['email'] = 'admi-n@admin.ru'

        response6 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response6.status_code, 201,
            msg='Неверный статус ответа при наличии дефиса в эмейле'
        )

    def test_wrong_password(self):
        data = {'email': 'admin@admin.ru', 'password': '1234567'}

        response1 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response1.status_code, 400,
            msg='Неверный статус ответа при вводе слишком короткого пароля'
        )

        data['password'] = '12345678901' * 4

        response2 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response2.status_code, 400,
            msg='Неверный статус ответа при вводе слишком длинного пароля'
        )

        data['password'] = '1234д5678'

        response3 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response3.status_code, 400,
            msg='Неверный статус ответа при наличии русских символов в пароле'
        )

    def test_no_body_in_request(self):
        data = {'password': '12345678'}

        response1 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response1.status_code, 400,
            msg='Неверный статус ответа при отсутствии эмейла в теле запроса'
        )

        data = {'email': 'admin@admin.ru'}

        response2 = self.client.post(reverse('signup'), data)
        self.assertEqual(
            response2.status_code, 400,
            msg='Неверный статус ответа при отсутствии пароля в теле запроса'
        )