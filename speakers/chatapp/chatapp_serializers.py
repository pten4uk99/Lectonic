from rest_framework import serializers

from chatapp.models import Chat, Message
from speakers.settings import DEFAULT_HOST


class ChatSerializer(serializers.ModelSerializer):
    lecture_name = serializers.SerializerMethodField()
    lecture_photo = serializers.SerializerMethodField()
    need_read = serializers.SerializerMethodField()
    respondent_id = serializers.SerializerMethodField()
    respondent_first_name = serializers.SerializerMethodField()
    respondent_last_name = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id',
            'lecture_name',
            'lecture_photo',
            'need_read',
            'respondent_id',
            'respondent_first_name',
            'respondent_last_name'
        ]

    def get_lecture_name(self, obj):
        return obj.lecture_request.lecture.name

    def get_need_read(self, obj):
        return Message.objects.filter(chat=obj, need_read=True).exclude(
            author=self.context['request'].user).exists()

    def get_lecture_photo(self, obj):
        if hasattr(obj.lecture_request, 'lecturer_lecture_request'):
            return DEFAULT_HOST + obj.lecture_request.lecturer_lecture_request.photo.url
        elif hasattr(obj.lecture_request, 'customer_lecture_request'):
            return DEFAULT_HOST + obj.lecture_request.customer_lecture_request.photo.url

    def get_respondent_id(self, obj):
        return obj.users.exclude(pk=self.context['request'].user.pk).first().pk

    def get_respondent_first_name(self, obj):
        return obj.users.exclude(pk=self.context['request'].user.pk).first().person.first_name

    def get_respondent_last_name(self, obj):
        return obj.users.exclude(pk=self.context['request'].user.pk).first().person.last_name


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(source='author.id')

    class Meta:
        model = Message
        fields = ['author', 'text', 'chat', 'datetime']
