from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField

User = get_user_model()


class City(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='')
    country = models.CharField(max_length=100, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.name}'


class Domain(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, default='no_name')
    code = models.CharField(max_length=100, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.name}'


class Person(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False, default='no_name')
    last_name = models.CharField(max_length=100, null=False, blank=False, default='no_lastname')
    middle_name = models.CharField(max_length=100, null=True, blank=True, default='')
    birth_date = models.DateField(null=False, blank=False, default=date.today)
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='person')
    address = models.CharField(max_length=200, null=True, blank=True, default='')
    rating = models.IntegerField(default=0, null=True, blank=True)
    photo = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    is_lecturer = models.BooleanField(default=False)
    is_project_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False) # Флаг для проверки модератором документов
    grade = models.CharField(max_length=300, null=True, blank=True, default='')
    description = models.TextField(null=True, blank=True)
    domain = models.OneToOneField(Domain, on_delete=models.CASCADE, related_name='person')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True,
                                          default='')  # Возможно надо будет добавить цифр, если будут ошибки поиска координат
    longtitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True,
                                            default='')  # Возможно надо будет добавить цифр, если будут ошибки поиска координат

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def isLecturer(self):
        if self.is_lecturer:
            return True
        else:
            return False


class Project(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, default='')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class ProjectLecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_lecturer')

    def __str__(self):
        return f'{self.user.email}'


class LectureHall(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='lecture_hall')
    area_size = models.IntegerField(default=0, null=True, blank=True)
    capacity = models.IntegerField(default=0, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecture_hall')
    has_whiteboard = models.BooleanField(default=False, null=True, blank=True)
    has_professional_sound = models.BooleanField(default=False, null=True, blank=True)
    has_transformer = models.BooleanField(default=False, null=True, blank=True)
    is_independent = models.BooleanField(default=False, null=True, blank=True)
    is_open = models.BooleanField(default=False, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True,
                                      default='')  # Возможно надо будет добавить цифр, если будут ошибки поиска координат
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True,
                                        default='')  # Возможно надо будет добавить цифр, если будут ошибки поиска координат

    def __str__(self):
        return f'{self.id}'


class Lecture(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    hall = models.OneToOneField(LectureHall, on_delete=models.CASCADE, null=True, blank=True, related_name='lecture')
    # cycle = models.ForeignKey(LectureCycle, on_delete=models.CASCADE, related_name='lecture')
    date = models.DateField(null=True, blank=True)
    duration = DateTimeRangeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    lecturer_name = models.CharField(max_length=300, null=True, blank=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True, blank=True, related_name='lecture')

    def __str__(self):
        return f'{self.name}'


# class LectureCycle(models.Model):
#     name = models.CharField(max_length=100, null=False, blank=False, unique=True)
#
#     def __str__(self):
#         return f'{self.name}'
#
#
# class LectureCycleProject(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     lecture_cycle = models.ForeignKey(LectureCycle, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'Проект - {self.project.name} Курс лекций - {self.lecture_cycle.name}' # Формат вывода, возможно, стоит изменить


# class Company(models.Model):
#     name = models.CharField(max_length=100, null=False, blank=False, default='no_name')
#     city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='company')
#     address = models.CharField(max_length=200, null=True, blank=True, default='')
#     inn = models.CharField(max_length=30, null=True, blank=True, default='', unique=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
#     is_project_admin = models.BooleanField(default=False)
#     is_customer = models.BooleanField(default=False)
#     is_verified = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.name}'


# class ProjectAdmin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
#     project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='project')
#
#     def __str__(self):
#         return f'{self.user.email}'

class Lecture_Lecturer(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lecture_lecturer')
    lectureId = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lecture_lecturer')

    def __str__(self):
        return 'ID пользователя - {} Лекция - {}'.format(self.userId.id,
                                                         self.lectureId.name)  # Формат вывода, возможно, стоит изменить
#
#
# class LectureListener(models.Model):
#     llistener_userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='llisteners')
#     llistener_lectureId = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='listener_lectures')
#
#     def __str__(self):
#         return 'ID пользователя - {} Лекция - {}'.format(self.llistener_userId.u_id,
#                                                          self.llistener_lectureId.lecture_name)  # Формат вывода, возможно, стоит изменить
#
#
# class LectureCustomer(models.Model):
#     lc_userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lcustomers')
#     lc_lectureId = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='customer_lectures')
#
#     def __str__(self):
#         return 'ID пользователя - {} Лекция - {}'.format(self.lc_userId.u_id,
#                                                          self.lc_lectureId.lecture_name)  # Формат вывода, возможно, стоит изменить
