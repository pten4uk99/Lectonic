from rest_framework import serializers

from chatapp.models import Chat, Message
from speakers.settings import DEFAULT_HOST


class ChatSerializer(serializers.ModelSerializer):
    lecture_name = serializers.SerializerMethodField()
    lecture_svg = serializers.SerializerMethodField()
    need_read = serializers.SerializerMethodField()
    respondent_id = serializers.SerializerMethodField()
    talker_online = serializers.SerializerMethodField()
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
            'talker_online',
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

    def get_talker_online(self, obj):
        talker_user = obj.users.exclude(pk=self.context['request'].user.pk).first()
        return hasattr(talker_user, 'ws_client')

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
