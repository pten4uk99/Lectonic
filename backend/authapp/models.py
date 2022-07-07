from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin

from rest_framework.authtoken.models import Token as BaseToken

from authapp.utils.authapp_managers import UserManager


class User(AbstractUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_authenticated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def login(self):
        self.is_authenticated = True
        self.save()
        return self, Token.objects.get_or_create(user=self)[0]

    def logout(self):
        self.is_authenticated = False
        self.auth_token.delete()
        self.save()
        return self


class Token(BaseToken):
    user = models.OneToOneField(
        User,
        related_name='auth_token',
        on_delete=models.CASCADE
    )
