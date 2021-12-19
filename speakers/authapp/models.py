from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields import EmailField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    u_id = models.CharField(max_length=30, null=False, blank=False, primary_key = True)
    u_login = models.CharField(_('login'), max_length=30, null=True, blank=True, unique=True)
    email = models.EmailField(_('email address'), null=False, blank=False, unique=True)
    u_isAdmin = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    u_phone = models.CharField(_('phone'), max_length=20, null=True, blank=True)
    u_rating = models.IntegerField(default = 0, null=True, blank=True)
    u_photo = models.CharField(_('photo link'), max_length=200, null=True, blank=True)
    u_date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
