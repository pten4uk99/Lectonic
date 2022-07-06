from authapp.models import User
from services.db import LectureObjectManager, LectureResponseManager
from services.types import AttrNames


class Service:
    """ Реализует бизнес логику проекта """

    object_manager = None

    def __init__(self, from_obj: User, from_attr: AttrNames = AttrNames.LECTURER):
        self.from_attr = from_attr
        self.from_obj = from_obj

        if self.object_manager is not None:
            self.object_manager = self.object_manager(from_attr)


class LectureService(Service):
    def __init__(self, from_obj: User, lecture_id: int = None, from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj, from_attr)

        if lecture_id is not None:
            self.lecture = LectureObjectManager().get_lecture_by_id(lecture_id)

    def check_permissions(self, *args, **kwargs) -> bool:
        """ Проверяет права """

        return True

    def to_do(self, *args, **kwargs) -> None:
        """ Метод для основной работы класса """

        pass

    def setup(self, *args, **kwargs) -> None:
        """ Собирает и запускает последовательно необходимые действия класса """

        self.check_permissions()
        self.to_do(*args, **kwargs)


class LectureResponseBaseService(LectureService):
    object_manager = LectureResponseManager
    chat_service = None

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        self.chat_service.setup()
