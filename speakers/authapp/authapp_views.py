from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView

from .authapp_serializers import (
    UserCreateSerializer,
    UserLoginSerializer
)
from .docs import authapp_docs
from .models import User
from .utils import authapp_responses


class CheckAuthenticationAPIView(APIView):
    @swagger_auto_schema(**authapp_docs.CheckAuthenticationDocs)
    def get(self, request):
        if not isinstance(request.user, User):
            return authapp_responses.unauthorized()
        return authapp_responses.success()


class UserCreationView(APIView):  # Возможно в будущем переделается на дженерик
    @swagger_auto_schema(**authapp_docs.UserProfileCreationView)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user, new_token = user.login()

        return authapp_responses.signed_in(
            data={'user': serializer.data['email']},
            cookie=('auth_token', new_token.key)
        )


class UserLoginView(APIView):
    @swagger_auto_schema(**authapp_docs.UserProfileLoginView)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user, new_token = serializer.get_object().login()

        return authapp_responses.logged_in(('auth_token', new_token.key))


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**authapp_docs.UserProfileLogoutView)
    def get(self, request):
        request.user.logout()
        return authapp_responses.logged_out('auth_token')


# --------------------Временные представления для разработки-----------------------

class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**authapp_docs.UserProfileDeleteView)
    def delete(self, request):
        request.user.delete()
        return authapp_responses.deleted('auth_token')

# --------------------Временные представления для разработки-----------------------
