from django.contrib.auth.middleware import AuthenticationMiddleware as BaseAuthMiddleware, get_user

from authapp.models import UserProfile
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject


def get_user_profile(request):
    user = None
    header = request.headers.get('Authorization')

    if header:
        try:
            token = header.split()[1]
            user = UserProfile.objects.filter(auth_token=token).first()
        except IndexError:
            return AnonymousUser()

    return user or AnonymousUser()


class AuthenticationMiddleware(BaseAuthMiddleware):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
        request.user_profile = get_user_profile(request)
