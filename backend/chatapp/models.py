from django.contrib.auth import get_user_model
from django.db import models

from workroomsapp.models import Lecture, LectureRequest

BaseUser = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(BaseUser, on_delete=models.CASCADE, unique=False)
    text = models.TextField()
    system_text = models.TextField(blank=True, null=True)
    chat = models.ForeignKey(
        'Chat',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    datetime = models.DateTimeField(auto_now_add=True)
    need_read = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.pk} {self.author.first_name}: {self.text[:40]}'


class Chat(models.Model):
    users = models.ManyToManyField(BaseUser, related_name='chat_list')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='chat_list')
    lecture_requests = models.ManyToManyField(LectureRequest, related_name='chat_list')
    confirm = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.pk} {self.users.all()}'


class WsClient(models.Model):
    channel_name = models.CharField(max_length=300, unique=True)
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='ws_client')
