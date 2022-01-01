import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import UserProfile, Token


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'u_email',
            'u_password',
            # повторный ввод пароля будет проверяться на стороне фронтенда
        )

    def validate_u_email(self, email):
        '''
        Валидация эмейла

        1. В строке может быть только один символ '@' и одна '.'
        2. До '@' могут быть любые буквы, цифры и '.'
        3. После '@' могут быть любые буквы и цифры
        4. После точки может быть от 2-х до 4-х латинских маленьких буквы
        5. В строке не может быть пробелов
        '''

        match = re.findall(r'^[\w.]+@\w+\.[a-z]{2,4}$', email)

        if not match:
            raise ValidationError('Некорректный эмейл')
        return email

    def validate_u_password(self, password):
        '''
        Валидация пароля

        1. Длина пароля от 8 символов
        '''

        # Для удобства в режиме разработки ограничение пароля только по длине
        match = re.findall(r'^.{8,}$', password)

        if not match:
            raise ValidationError('Пароль слишком короткий')
        return password


class UserProfileLoginSerializer(serializers.Serializer):
    u_email = serializers.EmailField()
    u_password = serializers.CharField()

    def get_object(self):
        ''' Из переданных данных получает объект пользователя '''
        return UserProfile.objects.get(u_email=self.validated_data.get('u_email'))

    def create_token(self):
        ''' Создает токен, относящийся к полученному пользователю '''
        user = self.get_object()
        return user, Token.objects.create(user=user)

    def login_user(self):
        ''' Аутентифицирует пользователя '''
        user, new_token = self.create_token()
        return user.login(), new_token
