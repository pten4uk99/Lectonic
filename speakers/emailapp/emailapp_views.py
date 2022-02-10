from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .emailapp_serializers import EmailSerializer
from .models import EmailConfirmation
from .responses.email_confirmation_responses import *
from .docs import emailapp_docs

from rest_framework.parsers import FormParser


class EmailConfirmationView(APIView):
    parser_classes = (FormParser,)

    @swagger_auto_schema(**emailapp_docs.EmailConfirmationDocCh1)
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']

        email_confirmation, created = EmailConfirmation.objects.get_or_create(email=email)

        if not created:
            if not email_confirmation.can_repeat_confirmation():
                return can_not_repeat_confirmation()

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

        if not key:
            return key_not_in_get()

        confirmation = EmailConfirmation.objects.filter(key=key).first()

        if confirmation and confirmation.check_lifetime():
            confirmation.confirmed = True
            confirmation.save()
            return confirmed(confirmation.email)

        if confirmation and not confirmation.check_lifetime():
            confirmation.delete()

        return bad_key()
