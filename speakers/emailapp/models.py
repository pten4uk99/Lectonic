import binascii
import datetime
import os

from django.db import models


class BaseEmailConfirmation(models.Model):
    email = models.EmailField(unique=True)
    key = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(7)).decode()

    def check_lifetime(self):
        return datetime.datetime.now() - self.created_at < datetime.timedelta(minutes=15)

    def can_repeat_confirmation(self):
        return datetime.datetime.now() - self.created_at > datetime.timedelta(seconds=30)

    def __str__(self):
        return self.key


class EmailConfirmation(BaseEmailConfirmation):
    pass


class EmailResetPassword(BaseEmailConfirmation):
    pass
