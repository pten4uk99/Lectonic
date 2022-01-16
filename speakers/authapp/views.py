from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .models import Person

from .serializers import (
    UserProfileCreateSerializer,
    UserProfileLoginSerializer
)


class UserProfileCreationView(APIView):  # Возможно в будущем переделается на дженерик
    def post(self, request):
        serializer = UserProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"user_profile": serializer.data['email'],
                  "status": "created"},
            status=201)


class UserProfileLoginView(APIView):
    def post(self, request):
        serializer = UserProfileLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, new_token = serializer.login_user()

        return Response(
            data={"auth_token": new_token.key,
                  "status": "logged_in"},
            status=201
        )


class UserProfileLogoutView(APIView):
    def post(self, request):
        user = request.user.logout()
        user.auth_token.delete()

        return Response(
            data={"status": "logged_out"},
            status=201
        )

def isLecturer(user):
    """Функция проверки пользователя является-ли он лектором"""
    pass

class AddLecture(APIView):
    def post(self, request):
        if (request.user.is_authenticated or request.user.is_staff):
            try:
                user = Person.objects.get(person_userProfileId = request.user.pk)
            except ObjectDoesNotExist:
                return Response(
                    data={"status":"error","description": "NoProfile","user_msg":"Необходимо заполнить профиль"},
                    status=500
                )
            if user.isLecturer:
                print(user)
                return Response(
                    data={"status":"ok"},
                    status=200
                )
            else:
                return Response(
                    data={"status":"error","description": "WrongAuthorization","user_msg":"Только лекторы могут добавлять лекции"},
                    status=403
                )
        else:
            return Response(
                data={"status":"error","description": "Unauthorized","user_msg":"Требуется авторизация"},
                status=401
            )
# --------------------Временные представления для разработки-----------------------


class UserProfileDeleteView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        request.user.delete()

        return Response(
            data={"status": "deleted"},
            status=201
        )


# Тестовая вьюшка для проверки аутентификации-----------------------
class TestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response(data={"response": "success"})

# --------------------Временные представления для разработки-----------------------
