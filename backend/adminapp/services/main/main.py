import os
import time
from datetime import datetime, timedelta

from adminapp.services import config
from adminapp.models import AuthCode

__all__ = [
    'main_api',
    'MainException',
]

from adminapp.services.main.context import ContextCreator, ListFilesParam, KeyParam, LastDumpChangeParam, UsersListParam

EARLIEST_ALLOWED_DATE = datetime.now() - timedelta(hours=2)


class MainException(Exception):
    pass


class IncorrectCode(MainException):
    pass


def check_correct_code(code: str) -> None:
    """ Проверяет корректность переданного кода """

    if not config.SIMPLE_ACCESS:
        auth_code = AuthCode.objects.filter(key=code).first()

        if not auth_code or auth_code.datetime < EARLIEST_ALLOWED_DATE:
            raise IncorrectCode()


def _get_filenames_list(dir_: str) -> list[str]:
    return os.listdir(dir_)


def _check_filename_limitations(filename: str) -> bool:
    if filename.startswith('__init__'):
        return False

    return True


def _make_context(code: str) -> dict:
    return ContextCreator([
        ListFilesParam(),
        KeyParam(code),
        LastDumpChangeParam(),
        UsersListParam()
    ]).context


def main_api(code: str) -> dict:
    check_correct_code(code)
    context = _make_context(code)
    return context
