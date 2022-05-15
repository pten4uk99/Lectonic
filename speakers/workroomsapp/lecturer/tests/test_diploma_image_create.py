from django.urls import reverse
from rest_framework.test import APITestCase, override_settings

from authapp.models import User
from speakers.utils.tests import data
from speakers.utils.tests.upload_image import test_image
from workroomsapp.models import City, Person, Domain, Lecturer


# @override_settings(MEDIA_URL=test_image.MEDIA_URL, MEDIA_ROOT=test_image.MEDIA_ROOT)
# class TestDiplomaImageCreate(APITestCase):
#     signup_data = data.SIGNUP.copy()
#     profile_data = data.PROFILE.copy()
#     lecturer_data = data.LECTURER.copy()
#
#     def setUp(self):
#         temp_signup_data = self.signup_data.copy()
#         temp_profile_data = self.profile_data.copy()
#         temp_profile_data['city'] = City.objects.create(pk=1, name='Москова')
#         temp_lecturer_data = self.lecturer_data.copy()
#
#         self.client.post(reverse('signup'), temp_signup_data)
#
#         user = User.objects.get(email=temp_signup_data['email'])
#         Person.objects.create(
#             user=user,
#             **temp_profile_data
#         )
#         Domain.objects.create(pk=1, name='Канцелярия')
#         Domain.objects.create(pk=2, name='Бухгалтерия')
#         Domain.objects.create(pk=3, name='Юриспруденция')
#
#         self.client.post(reverse('lecturer'), temp_lecturer_data)
#
#     def test_upload_diploma_images(self):
#         diploma1 = test_image.create_image(200, 300)
#         diploma2 = test_image.create_image(4500, 2000)
#         diploma3 = test_image.create_image(1920, 1090)
#
#         response1 = self.client.post(reverse('diploma_images'), {'diploma': diploma1})
#         response2 = self.client.post(reverse('diploma_images'), {'diploma': diploma2})
#         response3 = self.client.post(reverse('diploma_images'), {'diploma': diploma3})
#         print(response1.data)
#         print(response2.data)
#         print(response3.data)
