from utils import response

LECTURE_CREATED = 'Лекция успешно создана'
LECTURE_DELETED = 'Лекция успешно удалена'
LECTURE_DOES_NOT_EXIST = 'Данной лекции не существует'
RESPONDENT_DOES_NOT_EXIST = 'Выбранный пользователь не откликался на выбранную лекцию'
NOT_IN_DATA = 'Не переданы необходимые параметры'
DOES_NOT_EXIST = 'Лекции не существует'
FORBIDDEN = 'Откликаться на выбранные даты запрещено'
NOT_A_CREATOR = 'Пользователь не является создателем данной лекции'
NOT_A_RESPONDENT = 'Выбранный пользователь не откликался на выбранную лекцию'
CAN_NOT_RESPONSE = 'Пользователь не может откликнуться на данную лекцию'
CAN_NOT_CANCEL_RESPONSE = 'Пользователь не может отменить отклик на данную лекцию'
SUCCESS_RESPONSE = 'Вы успешно откликнулись на лекцию'
SUCCESS_CANCEL = 'Вы успешно отменили отклик на лекцию'
ERROR_CANCEL = 'Ошибка при отмене отклика. Чат не найден. ' \
               'Все чаты данной лекции с количеством пользователей меньше 2-х - удалены'
SUCCESS_CONFIRM = 'Отклик успешно подтвержден'
SUCCESS_DENIED = 'Отклик успешно отклонен'
LECTURER_FORBIDDEN = 'Только заказчик может откликнуться на эту лекцию'
CUSTOMER_FORBIDDEN = 'Только лектор может откликнуться на эту лекцию'

DESCRIPTION = '\n\nВсе возможные статусы ответов:\n' \
              f'"{response.SUCCESS}"\n' \
              f'"{response.CREATE}"\n' \
              f'"{response.EMPTY}"\n' \
              f'"{response.ERROR}"'


def lecture_created():
    return response.get_response(
        status=response.CREATE,
        detail=LECTURE_CREATED,
        status_code=201
    )


def lecture_deleted():
    return response.get_response(
        status=response.DELETE,
        detail=LECTURE_DELETED,
        status_code=200
    )


def not_in_data():
    raise response.ErrorException(detail=NOT_IN_DATA, status_code=400)


def forbidden():
    raise response.ErrorException(detail=FORBIDDEN, status_code=400)


def does_not_exist():
    raise response.ErrorException(detail=DOES_NOT_EXIST, status_code=400)


def lecturer_forbidden():
    raise response.ErrorException(detail=LECTURER_FORBIDDEN, status_code=400)


def customer_forbidden():
    raise response.ErrorException(detail=CUSTOMER_FORBIDDEN, status_code=400)


def success_response():
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS_RESPONSE,
        status_code=200
    )


def lecture_does_not_exist():
    raise response.ErrorException(detail=LECTURE_DOES_NOT_EXIST, status_code=400)


def success_cancel(data=None):
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS_CANCEL,
        data=data,
        status_code=200
    )


def error_cancel(data):
    return response.get_response(
        status=response.WARNING,
        detail=ERROR_CANCEL,
        data=data,
        status_code=200
    )


def not_a_creator():
    raise response.ErrorException(detail=NOT_A_CREATOR, status_code=400)


def not_a_respondent():
    raise response.ErrorException(detail=NOT_A_RESPONDENT, status_code=400)


def can_not_response():
    raise response.ErrorException(detail=CAN_NOT_RESPONSE, status_code=400)


def can_not_cancel_response():
    raise response.ErrorException(detail=CAN_NOT_CANCEL_RESPONSE, status_code=400)


def success_confirm():
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS_CONFIRM,
        status_code=200
    )


def success_denied():
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS_DENIED,
        status_code=200
    )


def success_get_lectures(data):
    return response.get_response(
        status=response.SUCCESS,
        data=data,
        status_code=200
    )
