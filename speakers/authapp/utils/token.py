from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication, get_authorization_header

from authapp.models import Token


class TokenAuthentication(BaseTokenAuthentication):
    model = Token

    def authenticate(self, request):
        token = get_authorization_header(request)

        try:
            token = token.decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        if not token:
            return None

        if ' ' in token:
            msg = _('Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        return token.user, token
