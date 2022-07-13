from datetime import timedelta

from django.http import SimpleCookie
from django.urls import reverse
from rest_framework.test import APITransactionTestCase

from config.utils.tests import data
from services.api import user_signup_service
from workroomsapp.models import City, Domain, LectureRequest, Lecture, Optional, Event, Calendar, LecturerCalendar, \
    CustomerCalendar, LectureDomain
from workroomsapp.tests.managers import get_str_range_datetime


class SignUpTestCase(APITransactionTestCase):
    """ Базовый класс для тестирования, в котором создается пользователь """

    signup_data = data.SIGNUP.copy()

    def setUp(self):
        super().setUp()
        user_login, serializer = user_signup_service(data=self.signup_data, pk=self.signup_data['pk'])
        self.client.cookies = SimpleCookie({'auth_token': user_login.token.key})


class PersonCreateTestCase(SignUpTestCase):
    """ Базовый класс для тестирования, в котором создается профиль пользователя """

    profile_data = data.PROFILE.copy()

    def setUp(self):
        super().setUp()
        self.profile_data['city'] = '1'
        City.objects.get_or_create(name='Москва', pk=1)
        temp_data = self.profile_data.copy()
        self.client.post(reverse('profile'), temp_data)


class BaseLecturerCreateTestCase(PersonCreateTestCase):
    """ Базовый класс для тестирования """

    lecturer_data = data.LECTURER.copy()

    def setUp(self):
        super().setUp()
        Domain.objects.get_or_create(pk=1, name='Канцелярия')
        Domain.objects.get_or_create(pk=2, name='Бухгалтерия')
        Domain.objects.get_or_create(pk=3, name='Юриспруденция')


class BaseCustomerCreateTestCase(BaseLecturerCreateTestCase):
    """ Базовый класс для тестирования """
    signup_data = data.SIGNUP2.copy()
    customer_data = data.CUSTOMER.copy()

    def setUp(self):
        super().setUp()


class CustomerCreateTestCase(BaseCustomerCreateTestCase):
    """ Базовый класс для тестирования, в котором создается профиль заказчика """

    def setUp(self):
        super().setUp()
        self.client.post(reverse('customer'), self.customer_data)


class LecturerCreateTestCase(BaseLecturerCreateTestCase):
    """ Базовый класс для тестирования, в котором создается профиль лектора """

    def setUp(self):
        super().setUp()
        self.client.post(reverse('lecturer'), self.lecturer_data)


class LectureTestCaseMixin:
    lecture_data = None

    def assertEqual(self, *args, **kwargs):
        # Используется только при наследовании
        pass

    def make_request(self, temp_data):
        # Используется только при наследовании
        pass

    def make_create_tests(self):
        # Для корректной работы используется только в классах-наследниках

        temp_data = self.lecture_data.copy()
        response = self.make_request(temp_data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании запроса на лекцию от лектора\n'
                f'Ответ: {response.data}'
        )

        self.assertEqual(
            LectureRequest.objects.all().exists(), True,
            msg='В базе не создан LectureRequest'
        )
        self.assertEqual(
            Lecture.objects.all().exists(), True,
            msg='В базе не создан Lecture'
        )
        self.assertEqual(
            Optional.objects.all().exists(), True,
            msg='В базе не создан Optional'
        )
        self.assertEqual(
            Event.objects.all().exists(), True,
            msg='В базе не создан Event'
        )
        self.assertEqual(
            Calendar.objects.all().exists(), True,
            msg='В базе не создан Calendar'
        )
        self.assertEqual(
            LecturerCalendar.objects.all().exists() or CustomerCalendar.objects.all().exists(), True,
            msg='В базе не создан LecturerCalendar и CustomerCalendar'
        )
        self.assertEqual(
            LectureDomain.objects.all().exists(), True,
            msg='В базе не создан LectureDomain'
        )
        self.assertEqual(
            hasattr(Lecture.objects.first(), 'lecture_requests'), True,
            msg='У созданной лекции нет аттрибута lecture_request'
        )

    def make_test_existing_datetime(self):
        # Для корректной работы используется только в классах-наследниках

        temp_data = self.lecture_data.copy()
        self.make_request(temp_data)

        response2 = self.make_request(temp_data)
        self.assertEqual(
            response2.status_code, 400,
            msg='Неверный статус ответа при создании события на существующую дату\n'
                f'Ответ: {response2.data}'
        )

        temp_data['datetime'] = [
            get_str_range_datetime(now_plus=timedelta(days=2, minutes=30),
                                   end_plus=timedelta(hours=2))
        ]
        response3 = self.make_request(temp_data)
        self.assertEqual(
            response3.status_code, 400,
            msg='Неверный статус ответа при создании события на существующую дату\n'
                f'Ответ: {response3.data}'
        )

        temp_data['datetime'] = [
            get_str_range_datetime(now_plus=timedelta(days=2, hours=1),
                                   end_plus=timedelta(hours=2))
        ]
        response4 = self.make_request(temp_data)
        self.assertEqual(
            response4.status_code, 201,
            msg='Неверный статус ответа при создании события на не существующую дату\n'
                f'Ответ: {response4.data}'
        )

        temp_data['datetime'] = [
            get_str_range_datetime(now_plus=timedelta(days=2, minutes=-15),
                                   end_plus=timedelta(minutes=15))
        ]
        response5 = self.make_request(temp_data)
        self.assertEqual(
            response5.status_code, 201,
            msg='Неверный статус ответа при создании события на не существующую дату\n'
                f'Ответ: {response5.data}'
        )

        temp_data['datetime'] = [
            get_str_range_datetime(now_plus=timedelta(days=2, minutes=-10),
                                   end_plus=timedelta(minutes=15))
        ]
        response6 = self.make_request(temp_data)
        self.assertEqual(
            response6.status_code, 400,
            msg='Неверный статус ответа при создании события на существующую дату\n'
                f'Ответ: {response6.data}'
        )


class BaseLectureAsLecturerCreateTestCase(LecturerCreateTestCase, LectureTestCaseMixin):
    """ Базовый класс для тестирования, в котором создается лекция от имени лектора """

    lecture_data = data.LECTURE.copy()

    def make_request(self, temp_data):
        response = self.client.post(reverse('lecture_as_lecturer'), temp_data)
        return response


class BaseLectureAsCustomerCreateTestCase(CustomerCreateTestCase, LectureTestCaseMixin):
    """ Базовый класс для тестирования, в котором создается лекция от имени заказчика """

    lecture_data = data.LECTURE_AS_CUSTOMER.copy()

    def make_request(self, temp_data):
        response = self.client.post(reverse('lecture_as_customer'), temp_data)
        return response
