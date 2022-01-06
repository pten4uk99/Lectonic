from django.db import models
from django.db.models.fields import EmailField
from django.utils import timezone
from datetime import date
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token as BaseToken


class UserProfile(models.Model):
    u_id = models.AutoField(null=False, blank=False, primary_key = True)
    u_login = models.CharField(max_length=30, null=True, blank=True, default='no login')
    u_password = models.CharField(max_length=100, null=False, blank=False)
    u_email = models.EmailField(max_length=254, null=False, blank=False, unique=True)
    u_phone = models.CharField(max_length=20, null=True, blank=True)
    u_activationKey = models.CharField(max_length=128, blank=True)
    u_activationKeyExpires = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    u_rating = models.IntegerField(default = 0, null=True, blank=True)
    u_photo = models.CharField(max_length=200, null=True, blank=True)
    u_isAdmin = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)

    def __str__(self):
        return self.u_login

    def save(self, *args, **kwargs):
        self.u_password = make_password(self.u_password)
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
    person_userProfileId = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name='person_user')
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
    pa_userProfileId = models.OneToOneField(UserProfile, on_delete = models.CASCADE, related_name='pa_user')
    pa_projectId = models.OneToOneField(Projects, on_delete = models.CASCADE, related_name='pa_project')

    def __str__(self):
        return self.pa_userId.u_login


class ProjectLecturer(models.Model):
    pu_lecturerId = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name='lecturers')
    pu_projectId = models.ForeignKey(Projects, on_delete = models.CASCADE, related_name='projects')

    def __str__(self):
        return self.pu_lecturerId.u_login


class Token(BaseToken):
    user = models.OneToOneField(
        UserProfile,
        related_name='auth_token',
        on_delete=models.CASCADE
    )
