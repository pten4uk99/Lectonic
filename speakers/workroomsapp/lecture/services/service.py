from authapp.models import User
from speakers.service import Service
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.db import DeleteLectureManager, AttrNames, LectureObjectManager

# logger = logging.getLogger(__name__)


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


class LectureDeleteService(LectureService):
    object_manager = DeleteLectureManager

    def check_permissions(self) -> bool:
        """ Проверяет является ли пользователь (self._from_obj), создателем лекции (lecture) """

        if self.lecture.lecturer:
            if not self.lecture.lecturer.person.user == self.from_obj:
                return lecture_responses.not_a_creator()
        elif self.lecture.customer:
            if not self.lecture.customer.person.user == self.from_obj:
                return lecture_responses.not_a_creator()

        return True

    def to_do(self) -> None:
        """ Удаляет объект Lecture из базы данных """

        self.object_manager.delete(self.lecture)

