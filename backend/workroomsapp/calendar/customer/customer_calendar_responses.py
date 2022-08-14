from utils import response

DOES_NOT_EXIST = 'Календарь заказчика не существует'


def success(data):
    return response.get_response(
        status=response.SUCCESS,
        data=data,
        status_code=200
    )


def does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail=DOES_NOT_EXIST,
        status_code=200
    )
