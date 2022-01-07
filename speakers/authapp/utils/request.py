from rest_framework import exceptions
from rest_framework.request import Request as BaseRequest


class Request(BaseRequest):
    def _authenticate(self):
        """
        Attempt to authenticate the request using each authentication instance
        in turn.
        """
        for authenticator in self.authenticators:
            try:
                user_auth_tuple = authenticator.authenticate(self)
            except exceptions.APIException:
                self._not_authenticated()
                raise

            if user_auth_tuple is not None:
                self._authenticator = authenticator
                self.user_profile, self.auth = user_auth_tuple
                return

        self._not_authenticated()
