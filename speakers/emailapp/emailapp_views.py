from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from authapp.models import User
from .emailapp_serializers import EmailSerializer
from .models import EmailConfirmation, EmailResetPassword
from .responses.email_confirmation_responses import *
from .docs import emailapp_docs

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


class EmailConfirmationView(APIView):
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    @swagger_auto_schema(**emailapp_docs.EmailConfirmationDocCh1)
    def post(self, request):
        reset_password = request.GET.get('reset_password')
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']

        if reset_password == 'true':
            email_confirmation, created = EmailResetPassword.objects.get_or_create(email=email)
        else:
            if User.objects.filter(email=email).first():
                return user_is_exist()

            email_confirmation, created = EmailConfirmation.objects.get_or_create(email=email)

        if not created:
            if not email_confirmation.can_repeat_confirmation():
                return can_not_repeat_confirmation()

        if reset_password == 'true':
            if User.objects.filter(email=email).first():
                html = render_to_string(
                    'emailapp/reset_password.html',
                    {
                        'key': email_confirmation.key,
                        'host': settings.DEFAULT_HOST
                    },
                )

                msg = EmailMultiAlternatives(
                    subject='Лектоник: Запрос на восстановление пароля',
                    to=[email]
                )

                msg.attach_alternative(html, 'text/html')
                msg.send()
        else:
            html = render_to_string(
                'emailapp/confirm_email.html',
                {
                    'key': email_confirmation.key,
                    'host': settings.DEFAULT_HOST
                },
            )

            msg = EmailMultiAlternatives(
                subject='Лектоник: Подтверждение регистрации нового пользователя',
                to=[email]
            )

            msg.attach_alternative(html, 'text/html')
            msg.send()

        return mail_is_sent()

    @swagger_auto_schema(**emailapp_docs.EmailConfirmationDocCh2)
    def get(self, request):
        key = request.GET.get('key')
        reset_password = request.GET.get('reset_password')

        if not key:
            return key_not_in_get()

        if reset_password == 'true':
            confirmation = EmailResetPassword.objects.filter(key=key).first()
        else:
            confirmation = EmailConfirmation.objects.filter(key=key).first()

        if confirmation and confirmation.confirmed:
            return confirmed([{'email': confirmation.email}])

        if confirmation and confirmation.check_lifetime():
            confirmation.confirmed = True
            confirmation.save()
            return confirmed([{'email': confirmation.email}])

        if confirmation and not confirmation.check_lifetime():
            confirmation.delete()

        return bad_key()
