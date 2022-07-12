import random

from django.db import models


class AuthCode(models.Model):
    key = models.IntegerField('Код')
    datetime = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return random.randint(100000, 999999)

    def __str__(self):
        return self.key
