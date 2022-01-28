from rest_framework.response import Response

LOGIN = 'logged_in'
LOGOUT = 'logged_out'
CREATED = 'created'
DELETED = 'deleted'
ERROR = 'error'


def get_response(status: str = "", detail: str = "",
                 data=None, status_code=None,
                 set_cookie: tuple = None, delete_cookie: str = None):

    if data is None:
        data = []

    response = Response(
        {
            "status": status,
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
