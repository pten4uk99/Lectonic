from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields import EmailField
# from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date
# from .managers import CustomUserManager

# class User(AbstractBaseUser, PermissionsMixin):
class User2(models.Model):
    u_id = models.AutoField(null=False, blank=False, primary_key = True)
    u_login = models.CharField(max_length=30, null=False, blank=False, unique=True, default='no login')
    u_password = models.CharField(max_length=100, null=False, blank=False)
    u_email = models.EmailField(null=True, blank=True, unique=True)
    u_phone = models.CharField(max_length=20, null=True, blank=True)
    u_rating = models.IntegerField(default = 0, null=True, blank=True)
    u_photo = models.CharField(max_length=200, null=True, blank=True)
    u_isAdmin = models.BooleanField(default=False)
    # USERNAME_FIELD = 'u_login'
    # REQUIRED_FIELDS = ['u_login','u_password']
    # objects = CustomUserManager()

    def __str__(self):
        return self.u_login

class City(models.Model):
    c_id = models.AutoField(null=False, blank=False, primary_key = True)
    c_name = models.CharField(max_length=100, null=True, blank=True, default='')
    c_country = models.CharField(max_length=100, null=True, blank=True, default='')

    def __str__(self):
        return self.c_name

class Person(models.Model):
    person_id = models.AutoField(null=False, blank=False, primary_key = True)
    person_firstName = models.CharField(max_length=100, null=False, blank=False, default='no name')
    person_lastname = models.CharField(max_length=100, null=False, blank=False, default='no lastname')
    person_middleName = models.CharField(max_length=100, null=True, blank=True, default='')
    person_birthdate = models.DateField(null=False, blank=False, default=date.today)
    person_cityId = models.OneToOneField(City, on_delete = models.CASCADE, related_name='person_city')
    person_address = models.CharField(max_length=200, null=True, blank=True, default='')
    person_userId = models.OneToOneField(User2, on_delete = models.CASCADE, related_name='person_user')
    person_isLecturer = models.BooleanField(default=False)
    person_isProjectAdmin = models.BooleanField(default=False)
    person_isCustomer = models.BooleanField(default=False)
    person_isVerified = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.person_firstName, self.person_lastname)

class Company(models.Model):
    company_id = models.AutoField(null=False, blank=False, primary_key = True)
    company_name = models.CharField(max_length=100, null=False, blank=False, default='no company name')
    company_cityId = models.OneToOneField(City, on_delete = models.CASCADE, related_name='company_city')
    company_address = models.CharField(max_length=200, null=True, blank=True, default='')
    company_inn = models.CharField(max_length=30, null=True, blank=True, default='', unique=True)
    company_userId = models.OneToOneField(User2, on_delete = models.CASCADE, related_name='company_user')
    company_isProjectAdmin = models.BooleanField(default=False)
    company_isCustomer = models.BooleanField(default=False)
    company_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

class Projects(models.Model):
    project_id = models.AutoField(null=False, blank=False, primary_key = True)
    project_name = models.CharField(max_length=200, null=True, blank=True, default='')
    project_description = models.TextField()

    def __str__(self):
        return self.project_name

class ProjectAdmin(models.Model):
    pa_userId = models.OneToOneField(User2, on_delete = models.CASCADE, related_name='pa_user')
    pa_projectId = models.OneToOneField(Projects, on_delete = models.CASCADE, related_name='pa_project')

    def __str__(self):
        return self.pa_userId.u_login

class ProjectLecturer(models.Model):
    pu_lecturerId = models.ForeignKey(User2, on_delete = models.CASCADE, related_name='lecturers')
    pu_projectId = models.ForeignKey(Projects, on_delete = models.CASCADE, related_name='projects')

    def __str__(self):
        return self.pu_lecturerId.u_login
    
