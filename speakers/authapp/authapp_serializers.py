import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from emailapp.models import EmailConfirmation
from .models import User, Token


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            # повторный ввод пароля будет проверяться на стороне фронтенда
        )

    def validate_email(self, email):
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

        # confirmation = EmailConfirmation.objects.filter(email=email).first()
        #
        # if not confirmation or (confirmation and not confirmation.confirmed):
        #     raise ValidationError('Данный адрес электронной почты не подтвержден')

        return email

    def validate_password(self, password):
        '''
        Валидация пароля

        1. Длина пароля от 8 символов
        2. Хотя бы одна заглавная буква, строчная буква, цифра
        3. Длина не более 40 знаков
        '''

        reg = r'^(?=.*[A-Z])(?=.*[\d])(?=.*[a-z]).{8,40}$'
        match = re.findall(reg, password)

        if not match:
            msg = 'Проверьте правильность ввода пароля'
            raise ValidationError(msg)

        return make_password(password)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def get_object(self):
        ''' Из переданных данных получает объект пользователя '''

        if self.context['request'].user.is_authenticated:
            raise serializers.ValidationError('Данный пользователь уже авторизован')

        user = User.objects.filter(email=self.initial_data.get('email')).first()
        return user

    def validate(self, data):
        user = self.get_object()

        if not user or not user.check_password(data['password']):
            raise serializers.ValidationError('Проверьте правильность ввода электронной почты или пароля')

        return data
