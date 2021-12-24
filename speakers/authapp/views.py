# === Base block ===
from .models import UserProfile
from django.shortcuts import render
# =================
# === DRF block ===
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError as VE
from rest_framework.response import Response
from rest_framework.views import APIView
#==================
from .serializers import UserCreateSerializer


def is_correct_login(login):
# Функция проверки логина: занят или нет, ... возможно будут другие проверки, например только английские буквы
    return True
def is_correct_email(email):
# Функция проверки почты: занята или нет, корректность и прочие проверки
    return True
def is_correct_passwd(passwd, passwd_repeat):
# Функция проверки пароля: совпадают ли пароль и повтор пароля, удовлетворяет ли пароль требованиям и прочие проверки
    return True

class Registration(APIView):
    def post(self, request):
        # Получаем данные из формы. Уточнить формат передачи данных из формы фронта
        u_login = request.data['login']
        u_email = request.data['email']
        u_password = request.data['pass']
        u_password_repeat = request.data['pass_repeat']
        if (is_correct_login(u_login) and is_correct_email(u_email) and is_correct_passwd(u_password, u_password_repeat)):
            new_user = UserProfile(u_login = u_login, u_email = u_email, u_password = u_password, u_isAdmin = False)
            try:
                new_user.save()
            except APIException:
                raise
            success = {'status_code':201,'usr_msg':'Регистрация прошла успешно'}
            return Response(success)


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------


class UserCreationView(APIView):  # Возможно в будущем переделается на дженерик
    def post(self, request):
        serializer = UserCreateSerializer(request.data)

        if serializer.is_valid(raise_exception=True):
            ''' Если валидация прошла, создаем пользователя '''
            pass
        return Response(status=201)
