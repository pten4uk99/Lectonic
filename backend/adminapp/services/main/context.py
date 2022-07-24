import os
import time
from abc import abstractmethod, ABC

from adminapp.services import config
from authapp.models import User


class ContextParam:
    """
    Базовый класс параметра контекста.

    При наследовании:
    name - имя параметра, передаваемого в шаблон
    get_value() - метод, возвращающий значение параметра

    Использование:
    Необходимо создать экземпляр класса для корректной работы,
    Если необходимо, можно при создании передать value - значение параметра,
    Если его не передать, то value будет получаться из self.get_value()
    """

    name: str

    def __init__(self, value=None):
        if value is not None:
            self.value = value
        else:
            self.value = self.get_value()

    @abstractmethod
    def get_value(self):
        """ Получает значение параметра контекста """


class ContextCreator:
    """
    Класс, отвечающий за создание контекста для шаблона

    Использование:
    Создаем экземпляр и передаем в него все дочерние экземпляры класса ContextParam.

    В переменной self.context будет храниться словарь контекста,
    который должен передаваться в шаблон.
    """

    def __init__(self, params: list[ContextParam]):
        self.params = params
        self.context = self.make_context()

    def make_context(self) -> dict:
        """
        Проходит по списку self.params,
        Для каждого элемента создает экземпляр класса,
        Добавляет в context полученные значения
        """

        context = {}

        for param in self.params:
            context[param.name] = param.value

        return context


class ListFilesParam(ContextParam):
    name = 'files'

    @staticmethod
    def _get_filenames_list(dir_: str) -> list[str]:
        return os.listdir(dir_)

    @staticmethod
    def _check_filename_limitations(filename: str) -> bool:
        if filename.startswith('__init__'):
            return False
        return True

    def get_value(self):
        value = []

        for filename in self._get_filenames_list(config.DIR):

            if not self._check_filename_limitations(filename):
                continue

            value.append({
                'path': config.DIR + filename,
                'filename': filename,
                'name': filename.split('.')[0]
            })

        return value


class KeyParam(ContextParam, ABC):
    """ При создании экземпляра, нужно передать value в инициализатор """

    name = 'key_param'

    def __init__(self, code):
        super().__init__(code)


class LastDumpChangeParam(ContextParam):
    """ Последнее изменение файла dbdump.json """

    name = 'last_dump_change'

    def get_value(self):
        value = None

        if os.path.exists(config.DUMP_PATH):
            value = time.ctime(os.path.getmtime(config.DUMP_PATH))

        return value


class UsersListParam(ContextParam):
    name = 'users'

    def get_value(self):
        return User.objects.all()
