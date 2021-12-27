from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication


from authapp.models import Token


class TokenAuthentication(BaseTokenAuthentication):
    model = Token

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        return token.user, token
