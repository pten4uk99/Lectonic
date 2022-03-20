from speakers.utils import response

UNAUTHORIZED = 'Пользователь не авторизован'
SUCCESS = 'Успешная проверка авторизации'
SIGNED_IN = 'Пользователь успешно зарегистрирован и авторизован'
LOGGED_IN = 'Пользователь успешно авторизован'
LOGGED_OUT = 'Пользователь успешно вышел из системы'
DELETED = 'Пользователь успешно удален'

DESCRIPTION = '\n\nВсе возможные статусы ответов:\n' \
              f'"{response.ERROR}"\n' \
              f'"{response.SIGN_IN}"\n' \
              f'"{response.LOGIN}"\n' \
              f'"{response.LOGOUT}"\n' \
              f'"{response.DELETE}"'


def unauthorized():
    return response.get_response(
        status=response.ERROR,
        detail=UNAUTHORIZED,
        status_code=401
    )


def success():
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS,
        status_code=200
    )


def success_check_auth(data):
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS,
        data=data,
        status_code=200
    )


def not_a_person(data):
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS,
        data=data,
        status_code=200
    )


def signed_in(data, cookie):
    return response.get_response(
        status=response.SIGN_IN,
        detail=SIGNED_IN,
        data=data,
        set_cookie=cookie,
        status_code=201
    )


def logged_in(cookie: tuple):
    return response.get_response(
        status=response.LOGIN,
        detail=LOGGED_IN,
        status_code=200,
        set_cookie=cookie
    )


def logged_out(cookie: str):
    return response.get_response(
        status=response.LOGOUT,
        detail=LOGGED_OUT,
        status_code=200,
        delete_cookie=cookie
    )


def deleted(cookie: str):
    return response.get_response(
        status=response.DELETE,
        detail=DELETED,
        status_code=200,
        delete_cookie=cookie
    )