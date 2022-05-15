from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView

from emailapp.models import EmailResetPassword
from .authapp_serializers import (
    UserCreateSerializer,
    UserLoginSerializer, CheckAuthenticationSerializer
)
from .docs import authapp_docs
from .models import User
from .utils import authapp_responses


class CheckAuthenticationAPIView(APIView):
    @swagger_auto_schema(**authapp_docs.CheckAuthenticationDocs)
    def get(self, request):
        if not isinstance(request.user, User):
            return authapp_responses.unauthorized()
        if not hasattr(request.user, 'person'):
            return authapp_responses.not_a_person([{
                'is_person': False,
                'is_lecturer': False,
                'is_customer': False
            }])

        serializer = CheckAuthenticationSerializer(request.user.person)
        return authapp_responses.success_check_auth([{
            **serializer.data,
            'is_person': True,
            'user_id': request.user.pk
        }])


class UserCreationView(APIView):
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

    @swagger_auto_schema(deprecated=True)
    def patch(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            return authapp_responses.not_in_data()

        user = User.objects.filter(email=email).first()

        if not user:
            return authapp_responses.does_not_exist()

        confirmation = EmailResetPassword.objects.filter(email=email).first()

        if not confirmation or (confirmation and not confirmation.confirmed):
            return authapp_responses.not_confirmed()

        user.set_password(password)
        user.save()

        return authapp_responses.success_change_password()


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
