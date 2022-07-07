from django.contrib import auth
from django.contrib.auth.middleware import AuthenticationMiddleware as BaseAuthMiddleware
from django.utils.functional import SimpleLazyObject

from authapp.utils.authapp_token import TokenAuthentication


def get_user_profile(request):
    authentication = TokenAuthentication()

    try:
        user, token = authentication.authenticate(request)
    except TypeError:
        return auth.get_user(request)

    return user


class AuthenticationMiddleware(BaseAuthMiddleware):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user_profile(request))
