from . import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

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
            data={"user_profile": serializer.data['u_email'],
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
        user = request.user_profile.logout()
        user.auth_token.delete()

        return Response(
            data={"status": "logged_out"},
            status=201
        )


# Тестовая вьюшка для проверки аутентификации-----------------------

class TestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response(data={"response": "success"})

# Тестовая вьюшка для проверки аутентификации-----------------------
