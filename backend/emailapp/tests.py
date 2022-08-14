from django.core import mail
from django.urls import reverse
from rest_framework.test import APITestCase

from emailapp.models import EmailConfirmation


class EmailTestCase(APITestCase):
    email = 'admin@test.py'

    def setUp(self):
        EmailConfirmation.objects.get_or_create(email=self.email)

    def test_email_confirmed(self):
        key = EmailConfirmation.objects.first().key
        response = self.client.get(reverse('email_confirmation'), {'key': key})
        self.assertEqual(
            response.status_code,
            200,
            msg='Неверный статус ответа при подтверждении почты'
                f'Ответ: {response.data}'
        )
