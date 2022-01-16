from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import DateTimeRangeField

from rest_framework.authtoken.models import Token as BaseToken

from .managers import UserProfileManager


class UserProfile(AbstractUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    activationKey = models.CharField(max_length=128, null=True, blank=True)
    activationKeyExpires = models.DateTimeField(auto_now_add=True, blank=True, null=True) # Жень, уточни параметр auto_now_add=True. Кажется это поле не должно быть по умолчанию "просроченым"
    is_authenticated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserProfileManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

    def login(self):
        self.is_authenticated = True
        self.save()
        return self

    def logout(self):
        self.is_authenticated = False
        self.save()
        return self


class City(models.Model):
    c_id = models.AutoField(null=False, blank=False, primary_key = True)
    c_name = models.CharField(max_length=100, null=True, blank=True, default='')
    c_country = models.CharField(max_length=100, null=True, blank=True, default='')

    def __str__(self):
        return self.c_name


class Domain(models.Model):
    domain_id = models.AutoField(null=False, blank=False, primary_key = True)
    domain_name = models.CharField(max_length=200, null=False, blank=False, default='no name')
    domain_code = models.CharField(max_length=100, null=True, blank=True, default='')

    def __str__(self):
        return self.domain_name


class Person(models.Model):
    person_id = models.AutoField(null=False, blank=False, primary_key = True)
    person_firstName = models.CharField(max_length=100, null=False, blank=False, default='no name')
    person_lastname = models.CharField(max_length=100, null=False, blank=False, default='no lastname')
    person_middleName = models.CharField(max_length=100, null=True, blank=True, default='')
    person_birthdate = models.DateField(null=False, blank=False, default=date.today)
    person_cityId = models.OneToOneField(City, on_delete = models.CASCADE, related_name='person_city')
    person_address = models.CharField(max_length=200, null=True, blank=True, default='')
    person_rating = models.IntegerField(default = 0, null=True, blank=True)
    person_photo = models.CharField(max_length=200, null=True, blank=True)
    person_userProfileId = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name='person_user')
    person_isListener = models.BooleanField(default=False)
    person_isLecturer = models.BooleanField(default=False)
    person_isProjectAdmin = models.BooleanField(default=False)
    person_isCustomer = models.BooleanField(default=False)
    person_isVerified = models.BooleanField(default=False)
    person_grade = models.CharField(max_length=300, null=True, blank=True, default='')
    person_description = models.TextField(null=True, blank=True)
    person_domainId = models.OneToOneField(Domain, on_delete = models.CASCADE, related_name='person_domain')
    person_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, default='') # Возможно надо будет добавить цифр, если будут ошибки поиска координат
    person_longtitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, default='') # Возможно надо будет добавить цифр, если будут ошибки поиска координат

    def __str__(self):
        return '{} {}'.format(self.person_firstName, self.person_lastname)
    
    def isLecturer(self):
        if self.person_isLecturer:
            return True
        else:
            return False 


class Company(models.Model):
    company_id = models.AutoField(null=False, blank=False, primary_key = True)
    company_name = models.CharField(max_length=100, null=False, blank=False, default='no company name')
    company_cityId = models.OneToOneField(City, on_delete = models.CASCADE, related_name='company_city')
    company_address = models.CharField(max_length=200, null=True, blank=True, default='')
    company_inn = models.CharField(max_length=30, null=True, blank=True, default='', unique=True)
    company_userProfileId = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name='company_user')
    company_isProjectAdmin = models.BooleanField(default=False)
    company_isCustomer = models.BooleanField(default=False)
    company_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class Projects(models.Model):
    project_id = models.AutoField(null=False, blank=False, primary_key = True)
    project_name = models.CharField(max_length=200, null=True, blank=True, default='')
    project_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.project_name


class ProjectAdmin(models.Model):
    pa_userId = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name='pa_user')
    pa_projectId = models.OneToOneField(Projects, on_delete = models.CASCADE, related_name='pa_project')

    def __str__(self):
        return self.pa_userId.u_email


class ProjectLecturer(models.Model):
    pu_lecturerId = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name='lecturers')
    pu_projectId = models.ForeignKey(Projects, on_delete = models.CASCADE, related_name='projects')

    def __str__(self):
        return self.pu_lecturerId.u_email


class Token(BaseToken):
    user = models.OneToOneField(
        UserProfile,
        related_name='auth_token',
        on_delete=models.CASCADE
    )


class LectureCycle(models.Model):
    lc_id = models.AutoField(null=False, blank=False, primary_key = True)
    lc_name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.lc_name


class LectureCycleProject(models.Model):
    lcp_projectId = models.ForeignKey(Projects, on_delete = models.CASCADE, related_name='lcp_projects')
    lcp_lectureCycleId = models.ForeignKey(LectureCycle, on_delete = models.CASCADE, related_name='lcp_lectureCycles')

    def __str__(self):
        return 'Проект - {} Курс лекций - {}'.format(self.lcp_projectId.project_name, self.lcp_lectureCycleId.lc_name)  # Формат вывода, возможно, стоит изменить


class LectureHall(models.Model):
    lh_id = models.AutoField(null=False, blank=False, primary_key = True)
    lh_cityId = models.OneToOneField(City, on_delete = models.CASCADE, related_name='lh_city')
    lh_areaSize = models.IntegerField(default = 0, null=True, blank= True)
    lh_capacity = models.IntegerField(default = 0, null=True, blank= True)
    lh_address = models.CharField(max_length=200, null=True, blank=True)
    lh_ownerId = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name='lh_owner')
    lh_hasWhiteboard = models.BooleanField(default=False)
    lh_hasProfessionalSound = models.BooleanField(default=False)
    lh_hasTransformer = models.BooleanField(default=False)
    lh_isIndependent = models.BooleanField(default=False)
    lh_isOpen = models.BooleanField(default=False)
    lh_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, default='') # Возможно надо будет добавить цифр, если будут ошибки поиска координат
    lh_longtitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, default='') # Возможно надо будет добавить цифр, если будут ошибки поиска координат

    def __str__(self):
        return self.lh_id


class Lecture(models.Model):
    lecture_id = models.AutoField(null=False, blank=False, primary_key = True)
    lecture_name = models.CharField(max_length=100, null=False, blank=False)
    lecture_hallId = models.OneToOneField(LectureHall, on_delete = models.CASCADE, related_name='lecture_hall')
    lecture_cycleId = models.ForeignKey(LectureCycle, on_delete = models.CASCADE, related_name='lectureCycles')
    lecture_date = models.DateField(null=True, blank=True)
    lecture_duration = DateTimeRangeField(null=True, blank=True)
    lecture_description = models.TextField(null=True, blank=True)
    lecture_lecturerName = models.CharField(max_length=300, null=True, blank=True)
    lecture_domainId = models.OneToOneField(Domain, on_delete = models.CASCADE, related_name='lecture_domain')

    def __str__(self):
        return self.lecture_name


class Lecture2_Lecturer(models.Model):
    llecturer_userId = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name='llecturers')
    llecturer_lectureId = models.ForeignKey(Lecture, on_delete = models.CASCADE, related_name='lecturer_lectures')
    
    def __str__(self):
        return 'ID пользователя - {} Лекция - {}'.format(self.llecturer_userId.u_id, self.llecturer_lectureId.lecture_name)  # Формат вывода, возможно, стоит изменить


class LectureListener(models.Model):
    llistener_userId = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name='llisteners')
    llistener_lectureId = models.ForeignKey(Lecture, on_delete = models.CASCADE, related_name='listener_lectures')
    
    def __str__(self):
        return 'ID пользователя - {} Лекция - {}'.format(self.llistener_userId.u_id, self.llistener_lectureId.lecture_name)  # Формат вывода, возможно, стоит изменить


class LectureCustomer(models.Model):
    lc_userId = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name='lcustomers')
    lc_lectureId = models.ForeignKey(Lecture, on_delete = models.CASCADE, related_name='customer_lectures')
    
    def __str__(self):
        return 'ID пользователя - {} Лекция - {}'.format(self.lc_userId.u_id, self.lc_lectureId.lecture_name)  # Формат вывода, возможно, стоит изменить