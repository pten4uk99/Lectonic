from rest_framework import serializers

from authapp.models import UserProfile


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'u_login',
            'u_email',
            'u_password',
            # повторный ввод пароля будет проверяться на стороне фронтенда
        )

    def validate_u_login(self, login):
        ''' Валидация логина '''
        return login

    def validate_u_email(self, email):
        ''' Валидация эмейла '''
        return email

    def validate_u_password(self, password):
        ''' Валидация пароля '''
        return password


class UserProfileLoginSerializer(serializers.Serializer):
    u_email = serializers.EmailField(required=False)
    u_password = serializers.CharField()

    def validate_u_email(self, email):
        ''' Валидация эмейла '''
        return email

    def validate_u_password(self, password):
        ''' Валидация пароля '''
        return password

