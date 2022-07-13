from django.db.models import Q
from rest_framework import serializers

from authapp.models import User
from chatapp.models import Chat, Message
from config.settings import DEFAULT_HOST
from services.types import user_id_type
from workroomsapp.models import Person


class ChatSerializer(serializers.ModelSerializer):
    lecture_name = serializers.SerializerMethodField()
    lecture_svg = serializers.SerializerMethodField()
    need_read = serializers.SerializerMethodField()
    respondent_id = serializers.SerializerMethodField()
    talker_id = serializers.SerializerMethodField()
    talker_first_name = serializers.SerializerMethodField()
    talker_last_name = serializers.SerializerMethodField()
    talker_photo = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id',
            'lecture_name',
            'lecture_svg',
            'need_read',
            'confirm',
            'respondent_id',
            'talker_id',
            'talker_first_name',
            'talker_last_name',
            'talker_photo',
        ]

    def get_lecture_name(self, obj):
        return obj.lecture.name

    def get_need_read(self, obj):
        return Message.objects.filter(chat=obj, need_read=True).exclude(
            author=self.context['user']).exists()

    def get_lecture_svg(self, obj):
        return obj.lecture.svg

    def get_respondent_id(self, obj):
        if obj.lecture.lecturer:
            return obj.lecture.lecturer.person.user.pk
        else:
            return obj.lecture.customer.person.user.pk

    def get_talker_id(self, obj):
        talker_user = obj.users.exclude(pk=self.context['user'].pk).first()
        return talker_user.pk

    def get_talker_first_name(self, obj):
        return obj.users.exclude(pk=self.context['user'].pk).first().person.first_name

    def get_talker_last_name(self, obj):
        return obj.users.exclude(pk=self.context['user'].pk).first().person.last_name

    def get_talker_photo(self, obj):
        photo = obj.users.exclude(pk=self.context['user'].pk).first().person.photo

        if photo:
            return DEFAULT_HOST + photo.url

        return ''


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(source='author.id')

    class Meta:
        model = Message
        fields = ['author', 'text', 'chat', 'datetime', 'system_text', 'need_read']


class ChatMessageListSerializer(serializers.ModelSerializer):
    lecture_id = serializers.SerializerMethodField()
    lecture_name = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()
    response_dates = serializers.SerializerMethodField()
    creator_is_lecturer = serializers.SerializerMethodField()
    talker_respondent = serializers.SerializerMethodField()
    talker_first_name = serializers.SerializerMethodField()
    talker_last_name = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'lecture_id',
            'lecture_name',
            'is_creator',
            'confirm',
            'response_dates',
            'creator_is_lecturer',
            'talker_respondent',
            'talker_first_name',
            'talker_last_name',
            'messages',
        ]

    def get_lecture_id(self, chat):
        return chat.lecture.pk

    def get_lecture_name(self, chat):
        return chat.lecture.name

    def get_is_creator(self, chat):
        lecture = chat.lecture

        is_creator = None

        if lecture.lecturer:
            is_creator = lecture.lecturer.person.user == self.context['user']
        elif lecture.customer:
            is_creator = lecture.customer.person.user == self.context['user']

        return is_creator

    def get_response_dates(self, chat):
        return chat.lecture_requests.all().values_list(
            'event__datetime_start', 'event__datetime_end')

    def get_creator_is_lecturer(self, chat):
        return bool(chat.lecture.lecturer)

    def _get_talker_user(self, chat: Chat) -> User:
        return chat.users.exclude(pk=self.context['user'].pk).first()

    def get_talker_respondent(self, chat) -> user_id_type:
        talker_user = self._get_talker_user(chat)
        return talker_user.pk

    def get_talker_first_name(self, chat):
        return self._get_talker_user(chat).person.first_name

    def get_talker_last_name(self, chat):
        return self._get_talker_user(chat).person.last_name

    def get_messages(self, chat):
        exclude_messages = chat.messages.values('id', 'system_text', 'author')
        exclude_ids = []

        for message in exclude_messages:
            if message['author'] == self.context['user'].pk and message['system_text']:
                exclude_ids.append(message['id'])

        messages = chat.messages.order_by('datetime').exclude(pk__in=exclude_ids)
        serializer = MessageSerializer(messages, many=True)
        return serializer.data
