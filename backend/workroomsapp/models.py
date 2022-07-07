from django.contrib.auth import get_user_model
from django.db import models

from config.utils.validators import PhotoValidator
from workroomsapp.customer.customer_manager import CustomerManager
from workroomsapp.lecture.lecture_manager import LectureManager
from workroomsapp.lecturer.lecturer_manager import LecturerManager
from workroomsapp.utils.paths_for_media import document_image, diploma_image, lecturer_lecture_image, person_image, \
    customer_lecture_image

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
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='customer_domains')  # заказчик
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE, related_name='customer_domains')  # сфера деятельности

    def __str__(self):
        return f'Сфера деятельности: {self.domain.name}. Заказчик: {self.customer.person.name}'


class LecturerDomain(models.Model):
    """Сфера деятельности лектора"""
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, related_name='lecturer_domains')  # лектор
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE, related_name='lecturer_domain')  # сфера деятельности

    def __str__(self):
        return f'Сфера деятельности: {self.domain.name}. Лектор: {self.company.person.name}'


class LectureDomain(models.Model):
    """Сфера деятельности лекции"""
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE, related_name='lecture_domains')
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE, related_name='lecture_domains')

    def __str__(self):
        return f'Сфера деятельности: {self.domain.name}. Лекция: {self.company.person.name}'


class DiplomaImage(models.Model):
    """Фотографии дипломов лектора"""
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, related_name='diploma_images')
    diploma = models.ImageField(upload_to=diploma_image)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.diploma:
            PhotoValidator(self.diploma.path).save()


class Person(models.Model):
    """Базовый профиль пользователя"""
    photo = models.ImageField(upload_to=person_image, null=True)
    bgc_number = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='person')
    rating = models.IntegerField(default=0)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            PhotoValidator(self.photo.path).save()


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
    company_name = models.CharField(max_length=250, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True, default='')
    company_site = models.CharField(max_length=200, blank=True, null=True)
    optional = models.OneToOneField(
        'Optional',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='customer'
    )
    objects = CustomerManager()
    # остальные поля исходят из других моделей к этой, так как ForeignKey


class CompanyForm(models.Model):
    """Форма юрлица: ОАО, ЗАО, ООО..."""
    name = models.CharField(max_length=100)


class Optional(models.Model):
    """Помещение, оборудование"""
    hall_address = models.CharField(max_length=200, blank=True, null=True)  # адрес помещения
    equipment = models.CharField(max_length=500, blank=True, null=True)  # перечисление имеющегося оборудования


class Respondent(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='respondent_obj')
    lecture_request = models.ForeignKey('LectureRequest', on_delete=models.CASCADE, related_name='respondent_obj')
    confirmed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)


class LectureRequest(models.Model):
    respondents = models.ManyToManyField('Person', through='Respondent', related_name='responses')
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE, related_name='lecture_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.lecture}, {self.respondents.all()}'


class Lecture(models.Model):
    """Лекция"""
    TYPES = [
        ('online', 'Онлайн'),
        ('offline', 'Офлайн'),
        ('hybrid', 'Гибрид')
    ]

    name = models.CharField(max_length=100)
    svg = models.IntegerField()  # id svg фотографии на фронтенде
    optional = models.OneToOneField(
        'Optional',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lecture'
    )
    type = models.CharField(max_length=20, choices=TYPES)
    listeners = models.IntegerField(blank=True, null=True)
    cost = models.IntegerField(default=0)  # стоимость лекции
    description = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='lectures',
        null=True,
        blank=True
    )
    lecturer = models.ForeignKey(
        'Lecturer',
        on_delete=models.CASCADE,
        related_name='lectures',
        null=True,
        blank=True
    )

    objects = LectureManager()

    def __str__(self):
        return f'{self.name}'


class Calendar(models.Model):
    """Общая модель календаря, у которой есть события"""
    events = models.ManyToManyField('Event')


class Event(models.Model):
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    lecture_request = models.OneToOneField('LectureRequest', on_delete=models.CASCADE, related_name='event')


class LecturerCalendar(models.Model):
    """Календарь лектора"""
    lecturer = models.OneToOneField('Lecturer', on_delete=models.CASCADE, related_name='lecturer_calendar')
    calendar = models.OneToOneField('Calendar', on_delete=models.CASCADE, related_name='lecturer_calendar')


class CustomerCalendar(models.Model):
    """Календарь заказчика: физлицо"""
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='customer_calendar')
    calendar = models.OneToOneField('Calendar', on_delete=models.CASCADE, related_name='customer_calendar')


# class DocumentImage(models.Model):
#     """Фотографии для подтверждения личности: фото паспорта и селфи с паспортом"""
#     person = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='document_image')  # связь к Person, потому что и у заказчика и у лектора документы одинаковые
#     passport = models.ImageField(upload_to=document_image)  # фото паспорта
#     selfie = models.ImageField(upload_to=document_image)  # селфи с паспортом
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.passport and self.selfie:
#             PhotoValidator(self.passport.path).save()
#             PhotoValidator(self.selfie.path).save()

