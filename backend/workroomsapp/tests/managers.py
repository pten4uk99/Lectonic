import datetime
from datetime import timedelta
from typing import Union

from authapp.models import User
from config.utils.tests import data
from workroomsapp.models import City, Person, Domain, Lecturer, Customer, Lecture


def get_str_range_datetime(now_plus: timedelta = timedelta(hours=0),
                           end_plus: timedelta = None,
                           end_minus: timedelta = None) -> str:
    """
    Принимает timedelta начала и конца промежутка даты и преобразовывает к строке вида:
    'YYYY-MM-DDThh:mm,YYYY-MM-DDThh:mm'
    """

    start = datetime.datetime.now() + now_plus

    if end_plus and end_minus:
        raise AttributeError('В функцию нельзя передать оба аргумента: (end_plus, end_minus)')
    if end_plus is not None:
        end = start + end_plus
    elif end_minus is not None:
        end = start - end_minus
    else:
        raise AttributeError('В функцию необходимо передать один из аргументов (end_plus, end_minus)')

    return start.strftime('%Y-%m-%dT%H:%M') + ',' + end.strftime('%Y-%m-%dT%H:%M')


class SignUpTestManager:
    _build_methods = []
    was_built = False
    signup_data = data.SIGNUP.copy()

    def __init__(self):
        self._user = None
        self._person = None
        self._lecturer = None
        self._customer = None

        self._build_methods = []

        for method in self.__dir__():
            if method.startswith('run'):
                self._build_methods.append(method)

    def _current_method(self):
        self.run_signup()

    def run_signup(self):
        self._user = User.objects.filter(email=self.signup_data['email']).first()

        if not self._user:
            self._user = User.objects.create(**self.signup_data)

    def create_obj(self):
        """ Проверяет созданы ли все зависимые объекты, и затем создает объект для текущего класса """

        if not self.was_built:
            for method_name in reversed(self._build_methods):
                getattr(self, method_name)()

            self.was_built = True
        else:
            self._current_method()


class PersonTestManager(SignUpTestManager):
    profile_data = data.PROFILE.copy()

    def run_person(self):
        City.objects.get_or_create(name='Москва', pk=1)
        self._person = Person.objects.create(**self.profile_data, user=self._user)
        # возможно в будущем лучше заменить прямое создание через ORM на создание через сериализатор

    def _current_method(self):
        self.run_person()


class LecturerTestManager(PersonTestManager):
    lecturer_data = data.LECTURER.copy()

    def run_lecturer(self):
        Domain.objects.get_or_create(pk=1, name='Канцелярия')
        Domain.objects.get_or_create(pk=2, name='Бухгалтерия')
        Domain.objects.get_or_create(pk=3, name='Юриспруденция')

        self._lecturer = Lecturer.objects.create_lecturer(
            **self.lecturer_data, person=self._person)

    def _current_method(self):
        self.run_lecturer()


class CustomerTestManager(PersonTestManager):
    signup_data = data.SIGNUP2.copy()
    customer_data = data.CUSTOMER.copy()

    def run_customer(self):
        Domain.objects.get_or_create(pk=1, name='Канцелярия')
        Domain.objects.get_or_create(pk=2, name='Бухгалтерия')
        Domain.objects.get_or_create(pk=3, name='Юриспруденция')

        self._customer = Customer.objects.create_customer(
            **self.customer_data, person=self._person)

    def _current_method(self):
        self.run_customer()


class LectureTestManager:
    data_as_lecturer = data.LECTURE.copy()
    data_as_customer = data.LECTURE_AS_CUSTOMER.copy()

    def __init__(self, creator: Union[Lecturer, Customer]):
        self._creator = creator
        self._creator_name = self._creator.__class__.__name__.lower()
        self._data = {}
        self._attrs = {self._creator_name: self._creator}

        if self._creator_name == 'lecturer':
            self._data = self.data_as_lecturer
        elif self._creator_name == 'customer':
            self._data = self.data_as_customer

        now = datetime.datetime.now().replace(second=0, microsecond=0)

        self._data['datetime'] = [
            [now + timedelta(days=2), now + timedelta(days=2, hours=1)],
            [now + timedelta(days=2, hours=2), now + timedelta(days=2, hours=3)],
            [now + timedelta(days=3, hours=2), now + timedelta(days=3, hours=3)],
        ]

    def create_obj(self, quantity: int = 1):
        for i in range(quantity):
            Lecture.objects.create_lecture(**self._data, **self._attrs)