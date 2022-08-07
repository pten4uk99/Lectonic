from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404

from adminapp.models import AuthCode

__all__ = [
    'auth_api'
]


class AuthException(Http404):
    pass


def _check_correct_email(email: str) -> None:
    for admin in settings.ADMINS:
        if admin[0] == 'Nikita':
            if email != admin[1]:
                raise AuthException()


def _make_auth_code() -> AuthCode:
    AuthCode.objects.all().delete()
    return AuthCode.objects.create()


def _send_code_on_email(email: str, code: str) -> None:
    """ Отправляет код на выбранный эмейл """

    send_mail(
        subject='Код доступа лектоник',
        message=str(code),
        recipient_list=[email],
        from_email=None
    )


def auth_api(email: str) -> None:
    """
    1. Проверяет, совпадает ли эмейлл с тем, что указан в переменной settings.ADMINS
    2. Если проверка прошла, то создает объект AuthCode
    3. Отправляет код на выбранный email.
    """

    _check_correct_email(email)
    auth_code = _make_auth_code()
    _send_code_on_email(email, auth_code.key)
