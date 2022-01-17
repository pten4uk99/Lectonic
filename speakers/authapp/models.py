from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin

from rest_framework.authtoken.models import Token as BaseToken

from .managers import UserProfileManager


class UserProfile(AbstractUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    activation_key = models.CharField(max_length=128, null=True, blank=True)
    activation_key_expires = models.DateTimeField(auto_now_add=True, blank=True, null=True) # Жень, уточни параметр auto_now_add=True. Кажется это поле не должно быть по умолчанию "просроченым"
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


class Token(BaseToken):
    user = models.OneToOneField(
        UserProfile,
        related_name='auth_token',
        on_delete=models.CASCADE
    )


