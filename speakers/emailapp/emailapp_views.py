from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView

from .models import EmailConfirmation
from .responses.email_confirmation_responses import *


class EmailConfirmationView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return email_not_in_data()

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
