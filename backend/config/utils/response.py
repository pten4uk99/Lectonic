from rest_framework.exceptions import APIException
from rest_framework.response import Response

CONFIRM = 'confirmed'
SIGN_IN = 'signed_in'
LOGIN = 'logged_in'
LOGOUT = 'logged_out'
SUCCESS = 'success'
CREATE = 'created'
EMPTY = 'empty'
DELETE = 'deleted'
ERROR = 'error'
WARNING = 'warning'

IS_LECTURER = '1'
IS_PROJECT_ADMIN = '2'
IS_CUSTOMER = '3'
IS_VERIFIED = '4'


def get_data(status, detail, data):

    if data is None:
        data = []

    return {
        "status": status,
        "detail": detail,
        "data": data
    }


def get_response(status: str = "", detail: str = "",
                 data=None, status_code=None,
                 set_cookie: tuple = None, delete_cookie: str = None):

    response = Response(get_data(status, detail, data), status=status_code)

    if set_cookie:
        response.set_cookie(set_cookie[0], set_cookie[1], samesite="None", secure=True, httponly=True)

    if delete_cookie:
        response.delete_cookie(delete_cookie)

    return response


class ErrorException(APIException):
    def __init__(self, detail: str = "", data=None, status_code=None):
        self.status_code = status_code
        self.detail = get_data(ERROR, detail, data)
