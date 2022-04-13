from django.contrib.auth import get_user_model
from django.db import models

from workroomsapp.models import Lecture

BaseUser = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(BaseUser, on_delete=models.CASCADE, unique=False)
    text = models.TextField()
    chat = models.ForeignKey(
        'Chat',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    datetime = models.DateTimeField(auto_now_add=True)
    need_read = models.BooleanField(default=True)
    confirm = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.pk} {self.author.first_name}: {self.text[:40]}'


class Chat(models.Model):
    users = models.ManyToManyField(BaseUser, related_name='chat_list')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='chat_list')

    def __str__(self):
        return f'{self.pk} {self.users.all()}'
