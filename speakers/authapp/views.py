from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    UserProfileCreateSerializer,
    UserProfileLoginSerializer
)
from .docs import docs


class UserProfileCreationView(APIView):  # Возможно в будущем переделается на дженерик
    @swagger_auto_schema(**docs.UserProfileCreationView)
    def post(self, request):
        serializer = UserProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"user_profile": serializer.data['email'],
                  "status": "created"},
            status=201)


class UserProfileLoginView(APIView):
    @swagger_auto_schema(**docs.UserProfileLoginView)
    def post(self, request):
        serializer = UserProfileLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, new_token = serializer.login_user()

        response = Response(
            data={
                "auth_token": new_token.key,
                "status": "logged_in"
            },
            status=201
        )

        response.set_cookie('auth_token', new_token.key, samesite="None", secure=True)
        return response


class UserProfileLogoutView(APIView):
    def post(self, request):
        user = request.user.logout()
        user.auth_token.delete()

        return Response(
            data={"status": "logged_out"},
            status=201
        )

# --------------------Временные представления для разработки-----------------------


class UserProfileDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
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
