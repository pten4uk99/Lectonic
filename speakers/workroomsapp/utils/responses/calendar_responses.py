from speakers.utils import response


def success(data):
    return response.get_response(
        status=response.CREATE,
        data=data,
        status_code=200
    )