from django.contrib.auth.middleware import AuthenticationMiddleware as BaseAuthMiddleware, get_user

from authapp.models import UserProfile
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject

from authapp.utils.token import TokenAuthentication


def get_user_profile(request):
    # token = request.headers.get('Authorization')
    auth = TokenAuthentication()
    try:
        user, token = auth.authenticate(request)
    except TypeError:
        return None

    # if token:
    #     try:
    #         user = UserProfile.objects.filter(auth_token=token).first()
    #     except IndexError:
    #         return AnonymousUser()

    return user


class AuthenticationMiddleware(BaseAuthMiddleware):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
        # request.user_profile = get_user_profile(request)
