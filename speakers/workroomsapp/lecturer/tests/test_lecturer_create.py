from django.urls import reverse
from rest_framework.test import APITestCase, override_settings

from authapp.models import User
from speakers.utils.tests import data
from speakers.utils.tests.upload_image import test_image
from workroomsapp.models import City, Person, Domain, Lecturer


@override_settings(MEDIA_URL=test_image.MEDIA_URL, MEDIA_ROOT=test_image.MEDIA_ROOT)
class TestLecturerCreate(APITestCase):
    signup_data = data.SIGNUP.copy()
    profile_data = data.PROFILE.copy()
    lecturer_data = data.LECTURER.copy()

    def setUp(self):
        temp_signup_data = self.signup_data.copy()
        temp_profile_data = self.profile_data.copy()
        temp_profile_data['city'] = City.objects.create(pk=1, name='Москова')

        self.client.post(reverse('signup'), temp_signup_data)

        user = User.objects.get(email=temp_signup_data['email'])
        Person.objects.create(
            user=user,
            **temp_profile_data
        )
        Domain.objects.create(pk=1, name='Канцелярия')
        Domain.objects.create(pk=2, name='Бухгалтерия')
        Domain.objects.create(pk=3, name='Юриспруденция')

    def test_lecturer_was_created(self):
        temp_data = self.lecturer_data.copy()
        response = self.client.post(reverse('lecturer'), temp_data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании профиля лектора'
        )
        self.assertEqual(
            Lecturer.objects.filter(person=Person.objects.get(user=User.objects.first())).exists(),
            True,
            msg='Лектор не был создан в базе данных'
        )

    def test_credentials(self):
        temp_data = self.lecturer_data.copy()
        self.client.get(reverse('logout'))

        response = self.client.post(reverse('lecturer'), temp_data)
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке создания профиля лектора неавторизованным пользователем'
        )

    def test_wrong_domain(self):
        temp_data = self.lecturer_data.copy()
        temp_data['domain'] = ['privet']

        response = self.client.post(reverse('lecturer'), temp_data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при неверно переданной тематике лекции'
        )
