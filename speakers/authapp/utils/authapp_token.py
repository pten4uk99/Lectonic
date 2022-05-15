from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication

from authapp.models import Token


def get_auth_token(request):
    token = request.COOKIES.get('auth_token')

    # Тут предполагаются какие-либо проверки токена в будущем

    return token


class TokenAuthentication(BaseTokenAuthentication):
    model = Token

    def authenticate(self, request):
        token = get_auth_token(request)

        if not token:
            return None

        if ' ' in token:
            raise exceptions.AuthenticationFailed('Недопустимый токен')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            return None

        return token.user, token
