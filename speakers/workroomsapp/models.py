from statistics import mode

import datetime as datetime
from django.contrib.auth import get_user_model
from django.db import models

from workroomsapp.utils.workroomsapp_managers import LectureManager, CustomerManager, LecturerManager, CompanyManager

BaseUser = get_user_model()


class City(models.Model):
    """Город"""
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Domain(models.Model):
    """Cфера деятельности (химия, биология, физика)"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class CustomerDomain(models.Model):
    """Сфера деятельности заказчика: физлицо"""
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)  # заказчик
    domain = models.OneToOneField('Domain', on_delete=models.CASCADE)  # сфера деятельности

    def __str__(self):
        return f'Сфера деятельности: {self.domain.name}. Заказчик: {self.customer.person.name}'


class CompanyDomain(models.Model):
    """Сфера деятельности заказчика: юрлицо"""
    company = models.ForeignKey('Company', on_delete=models.CASCADE)  # компания
    domain = models.OneToOneField('Domain', on_delete=models.CASCADE)  # сфера деятельности

    def __str__(self):
        return f'Сфера деятельности: {self.domain.name}. Заказчик: {self.company.person.name}'


class LecturerDomain(models.Model):
    """Сфера деятельности лектора"""
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, related_name='lecturer_domains')  # лектор
    domain = models.OneToOneField('Domain', on_delete=models.CASCADE, related_name='lecturer_domain')  # сфера деятельности

    def __str__(self):
        return f'Сфера деятельности: {self.domain.name}. Лектор: {self.company.person.name}'


class LectureDomain(models.Model):
    """Сфера деятельности лекции"""
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE)  # лекция
    domain = models.OneToOneField('Domain', on_delete=models.CASCADE)  # сфера деятельности

    def __str__(self):
        return f'Сфера деятельности: {self.domain.name}. Лекция: {self.company.person.name}'


class Image(models.Model):
    """Изображение"""
    photo = models.ImageField()  # надо подумать как и куда загружать


class DocumentImage(models.Model):
    """Фотографии для подтверждения личности: фото паспорта и селфи с паспортом"""
    person = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='document_image')  # связь к Person, потому что и у заказчика и у лектора документы одинаковые
    passport = models.OneToOneField('Image', on_delete=models.CASCADE, related_name='document_image')  # фото паспорта
    selfie = models.OneToOneField('Image', on_delete=models.CASCADE)  # селфи с паспортом


class DiplomaImage(models.Model):
    """Фотографии дипломов лектора"""
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, related_name='diploma_image')
    image = models.OneToOneField('Image', on_delete=models.CASCADE, related_name='diploma_image')


class Person(models.Model):
    """Базовый профиль пользователя"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='person')
    rating = models.IntegerField(default=0)
    # photo = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='person')
    is_lecturer = models.BooleanField(default=False)
    is_project_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # Флаг для проверки модератором документов
    description = models.TextField(blank=True, default='')
    latitude = models.DecimalField(
        max_digits=10,  # Возможно надо будет добавить цифр, если будут ошибки поиска координат
        decimal_places=7,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=10,  # Возможно надо будет добавить цифр, если будут ошибки поиска координат
        decimal_places=7,
        null=True,
        blank=True
    )
    sys_created_at = models.DateTimeField(auto_now_add=True)
    sys_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Lecturer(models.Model):
    """Лектор"""
    person = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='lecturer')
    performances_links = models.ManyToManyField('Link', related_name='perf_lecturer')  # ссылки на выступления. Лекторы могут выступать по двое, поэтому ManyToMany
    publication_links = models.ManyToManyField('Link', related_name='pub_lecturer')  # ссылки на публикации. Так же, у публикации может быть несколько авторов
    education = models.TextField(blank=True, null=True)
    optional = models.OneToOneField(
        'Optional',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='lecturer'
    )

    objects = LecturerManager()


class Link(models.Model):
    """Ссылка"""
    url = models.URLField()


class Customer(models.Model):
    """Заказчик: физлицо"""
    person = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='customer')
    optional = models.OneToOneField(
        'Optional',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='customer'
    )
    objects = CustomerManager()
    # остальные поля исходят из других моделей к этой, так как ForeignKey


class Company(models.Model):
    """Заказчик: юрлицо"""
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # название организации
    company_form = models.ForeignKey('CompanyForm', on_delete=models.CASCADE, null=True, blank=True)  # ЗАО, ООО, ОАО
    specialization = models.TextField(null=True, blank=True)  # описание специализации компании
    document = models.OneToOneField('Image', on_delete=models.CASCADE)
    representative_person = models.OneToOneField(
        'RepresentativePerson',
        on_delete=models.CASCADE,
        related_name='company'
    )  # представитель организации
    legal_address = models.CharField(max_length=200)  # юридический адрес
    actual_address = models.CharField(max_length=200)  # фактический адрес
    optional = models.OneToOneField(
        'Optional',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='company'
    )
    is_verified = models.BooleanField(default=False)

    objects = CompanyManager()

    def __str__(self):
        return f'{self.name}'


class CompanyForm(models.Model):
    """Форма юрлица: ОАО, ЗАО, ООО..."""
    name = models.CharField(max_length=100)


class RepresentativePerson(models.Model):
    """Умолномоченный представитель юрлица"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)


class OptionalImage(models.Model):
    optional = models.ForeignKey('Optional', on_delete=models.CASCADE, related_name='optional_images')
    photo = models.OneToOneField('Image', on_delete=models.CASCADE)


class Optional(models.Model):  # помещение, оборудование
    hall_address = models.CharField(max_length=200, blank=True, null=True)  # адрес помещения
    equipment = models.CharField(max_length=500, blank=True, null=True)  # перечисление имеющегося оборудования


class Respondent(models.Model):
    """Откликнувшийся на заявку на лекцию"""
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)


class LectureRequest(models.Model):
    respondents = models.ManyToManyField('Respondent', related_name='lecture_requests')
    lecture = models.OneToOneField('Lecture', on_delete=models.CASCADE, related_name='lecture_request')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class LecturerLectureRequest(models.Model):
    lecture_request = models.OneToOneField(
        'LectureRequest',
        on_delete=models.CASCADE,
        related_name='lecturer_lecture_request'
    )
    lecturer = models.ForeignKey(
        'Lecturer',
        on_delete=models.CASCADE,
        related_name='lecturer_lecture_request'
    )


class CustomerLectureRequest(models.Model):
    lecture_request = models.OneToOneField(
        'LectureRequest',
        on_delete=models.CASCADE,
        related_name='customer_lecture_request')
    customer = models.OneToOneField(
        'Customer',
        on_delete=models.CASCADE,
        related_name='customer_lecture_request'
    )


class CompanyLectureRequest(models.Model):
    lecture_request = models.OneToOneField(
        'LectureRequest',
        on_delete=models.CASCADE,
        related_name='company_lecture_request'
    )
    company = models.OneToOneField(
        'Company',
        on_delete=models.CASCADE,
        related_name='company_lecture_request'
    )


class Lecture(models.Model):
    """Лекция"""
    name = models.CharField(max_length=100)
    optional = models.OneToOneField(
        'Optional',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lecture'
    )
    status = models.BooleanField(null=True, blank=True)  # 3 варианта: подтверждена, отклонена, не просмотрена
    duration = models.IntegerField(null=True, blank=True)  # Длительность лекции в минутах (нет необходимости использовать DateTimeRangeField)
    cost = models.IntegerField(default=0)  # стоимость лекции
    description = models.TextField(null=True, blank=True)

    objects = LectureManager()

    def __str__(self):
        return f'{self.name}'


class Calendar(models.Model):
    """Общая модель календаря, у которой есть события"""
    events = models.ManyToManyField('Event')


class Event(models.Model):
    datetime = models.DateTimeField()
    event = models.ForeignKey('LectureRequest', on_delete=models.CASCADE, related_name='events')


class LecturerCalendar(models.Model):
    """Календарь лектора"""
    lecturer = models.OneToOneField('Lecturer', on_delete=models.CASCADE, related_name='lecturer_calendar')
    calendar = models.OneToOneField('Calendar', on_delete=models.CASCADE, related_name='lecturer_calendar')


class CustomerCalendar(models.Model):
    """Календарь заказчика: физлицо"""
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='customer_calendar')
    calendar = models.OneToOneField('Calendar', on_delete=models.CASCADE, related_name='customer_calendar')


class CompanyCalendar(models.Model):
    """Календарь заказчика: юрлицо"""
    company = models.OneToOneField('Company', on_delete=models.CASCADE, related_name='company_calendar')
    calendar = models.OneToOneField('Calendar', on_delete=models.CASCADE, related_name='company_calendar')

