from rest_framework import serializers

from .models import UserProfile, Token


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
    u_login = serializers.CharField(required=False)
    u_email = serializers.EmailField(required=False)
    u_password = serializers.CharField()

    def validate_u_login(self, login):
        ''' Валидация логина '''
        return login

    def validate_u_email(self, email):
        ''' Валидация эмейла '''
        return email

    def validate_u_password(self, password):
        ''' Валидация пароля '''
        return password

    def get_object(self):
        ''' Из переданных данных получает объект пользователя '''
        return UserProfile.objects.get(u_login=self.validated_data.get('u_login'))

    def create_token(self):
        ''' Создает токен, относящийся к полученному пользователю '''
        user = self.get_object()
        return user, Token.objects.create(user=user)

    def login_user(self):
        ''' Аутентифицирует пользователя '''
        user, new_token = self.create_token()
        return user.login(), new_token
