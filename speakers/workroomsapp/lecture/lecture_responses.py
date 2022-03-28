from speakers.utils import response

LECTURE_CREATED = 'Лекция успешно создана'
LECTURE_DOES_NOT_EXIST = 'Данной лекции не существует'
RESPONDENT_DOES_NOT_EXIST = 'Выбранный пользователь не откликался на выбранную лекцию'
NOT_IN_DATA = 'Не переданы необходимые параметры'
NOT_A_CREATOR = 'Пользователь не является создателем данной лекции'
NOT_A_RESPONDENT = 'Выбранный пользователь не откликался на выбранную лекцию'
SUCCESS_RESPONSE = 'Вы успешно откликнулись на лекцию'
SUCCESS_CANCEL = 'Вы успешно отменили отклик на лекцию'
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


def not_in_data():
    return response.get_response(
        status=response.ERROR,
        detail=NOT_IN_DATA,
        status_code=400
    )


def lecturer_forbidden():
    return response.get_response(
        status=response.ERROR,
        detail=LECTURER_FORBIDDEN,
        status_code=400
    )


def customer_forbidden():
    return response.get_response(
        status=response.ERROR,
        detail=CUSTOMER_FORBIDDEN,
        status_code=400
    )


def success_response():
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS_RESPONSE,
        status_code=200
    )


def lecture_does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail=LECTURE_DOES_NOT_EXIST,
        status_code=400
    )


def success_cancel():
    return response.get_response(
        status=response.SUCCESS,
        detail=SUCCESS_CANCEL,
        status_code=200
    )


def not_a_creator():
    return response.get_response(
        status=response.ERROR,
        detail=NOT_A_CREATOR,
        status_code=400
    )


def not_a_respondent():
    return response.get_response(
        status=response.ERROR,
        detail=NOT_A_RESPONDENT,
        status_code=400
    )


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

