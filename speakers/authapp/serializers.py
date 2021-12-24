from rest_framework import serializers

from authapp.models import UserProfile


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'u_login',
            'u_email',
            'u_password',
            'u_password_repeat'
        )

    def validate_u_login(self, data):
        ''' Валидация логина '''
        return data

    def validate_u_email(self, data):
        ''' Валидация эмейла '''
        return data

    def validate_u_password(self, data):
        ''' Валидация пароля +
        тут же проверка на равенство повторному паролю '''
        return data
