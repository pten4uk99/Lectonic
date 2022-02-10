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

IS_LECTURER = '1'
IS_PROJECT_ADMIN = '2'
IS_CUSTOMER = '3'
IS_VERIFIED = '4'


def get_response(status: str = "", detail: str = "",
                 data=None, status_code=None,
                 set_cookie: tuple = None, delete_cookie: str = None,
                 perms: list = None):
    if data is None:
        data = []

    if perms is None:
        perms = []

    response = Response(
        {
            "status": status,
            # "need_perms": perms,
            "detail": detail,
            "data": data
        },
        status=status_code
    )

    if set_cookie:
        response.set_cookie(set_cookie[0], set_cookie[1], samesite="None", secure=True, httponly=True)

    if delete_cookie:
        response.delete_cookie(delete_cookie)

    return response
