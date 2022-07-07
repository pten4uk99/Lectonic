from django.db.models import Q
from rest_framework import serializers

from chatapp.models import Chat, Message
from config.settings import DEFAULT_HOST
from workroomsapp.models import Person


class ChatSerializer(serializers.ModelSerializer):
    lecture_name = serializers.SerializerMethodField()
    lecture_svg = serializers.SerializerMethodField()
    need_read = serializers.SerializerMethodField()
    respondent_id = serializers.SerializerMethodField()
    talker_id = serializers.SerializerMethodField()
    talker_first_name = serializers.SerializerMethodField()
    talker_last_name = serializers.SerializerMethodField()
    chat_confirm = serializers.SerializerMethodField()
    talker_photo = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id',
            'lecture_name',
            'lecture_svg',
            'need_read',
            'respondent_id',
            'talker_id',
            'talker_first_name',
            'talker_last_name',
            'talker_photo',
            'chat_confirm'
        ]

    def get_lecture_name(self, obj):
        return obj.lecture.name

    def get_need_read(self, obj):
        return Message.objects.filter(chat=obj, need_read=True).exclude(
            author=self.context['request'].user).exists()

    def get_lecture_svg(self, obj):
        return obj.lecture.svg

    def get_chat_confirm(self, obj):
        for confirmed in obj.messages.all().values_list('confirm', flat=True):
            if confirmed:
                return confirmed
            elif confirmed is not None and not confirmed:
                return confirmed
        return None

    def get_respondent_id(self, obj):
        if obj.lecture.lecturer:
            return obj.lecture.lecturer.person.user.pk
        else:
            return obj.lecture.customer.person.user.pk

    def get_talker_id(self, obj):
        talker_user = obj.users.exclude(pk=self.context['request'].user.pk).first()
        return talker_user.pk

    def get_talker_first_name(self, obj):
        return obj.users.exclude(pk=self.context['request'].user.pk).first().person.first_name

    def get_talker_last_name(self, obj):
        return obj.users.exclude(pk=self.context['request'].user.pk).first().person.last_name

    def get_talker_photo(self, obj):
        photo = obj.users.exclude(pk=self.context['request'].user.pk).first().person.photo

        if photo:
            return DEFAULT_HOST + photo.url

        return ''


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(source='author.id')

    class Meta:
        model = Message
        fields = ['author', 'text', 'chat', 'datetime', 'confirm', 'need_read']


class MessageListSerializer(serializers.ModelSerializer):
    lecture_id = serializers.StringRelatedField(source='chat.lecture.pk'),
    lecture_name = serializers.StringRelatedField(source='chat.lecture.name'),
    is_creator = serializers.SerializerMethodField(),
    confirmed = serializers.SerializerMethodField(),
    response_dates = serializers.SerializerMethodField(),
    talker_respondent = serializers.SerializerMethodField(),
    talker_first_name = serializers.SerializerMethodField(),
    talker_last_name = serializers.SerializerMethodField(),
    messages = MessageSerializer(),

    class Meta:
        model = Message
        fields = [
            'lecture_id',
            'lecture_name',
            'is_creator',
            'confirmed',
            'response_dates',
            'talker_respondent',
            'talker_first_name',
            'talker_last_name',
            'messages',
        ]

    def get_is_creator(self, message):
        lecture = message.chat.lecture

        is_creator = None

        if lecture.lecturer:
            is_creator = lecture.lecturer.person.user == self.context['user']
        elif lecture.customer:
            is_creator = lecture.customer.person.user == self.context['user']

        return is_creator

    def get_confirmed(self, message):
        chat = message.chat
        message = chat.messages.filter(Q(confirm=True) | Q(confirm=False)).first()

        if message is not None:
            return message.confirm
        return None

    def get_response_dates(self, message):
        return message.chat.lecture_requests.all().values_list(
            'event__datetime_start', 'event__datetime_end')

    def _get_talker_person(self, message: Message) -> Person:
        return message.chat.users.exclude(pk=self.context['user'].pk).first().person

    def get_talker_respondent(self, message):
        talker_person = self._get_talker_person(message)
        is_creator = self.get_is_creator(message)

        respondent: int

        if is_creator:
            # если пользователь является создателем лекции, то откликнувшийся - собеседник чата
            respondent = talker_person.pk
        else:
            # иначе сам пользователь - откликнувшийся
            respondent = self.context['user'].pk

        return respondent

    def get_talker_first_name(self, message):
        return self._get_talker_person(message).first_name

    def get_talker_last_name(self, message):
        return self._get_talker_person(message).last_name
