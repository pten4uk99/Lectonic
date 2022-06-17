import datetime
from enum import Enum

from django.db.models import QuerySet, Max

from authapp.models import User
from chatapp.models import Chat, Message
from workroomsapp.lecture import lecture_responses
from workroomsapp.models import Person, Lecture, LectureRequest


class AttrNames(Enum):
    LECTURER = 'lecturer'
    CUSTOMER = 'customer'


class LectureObjectManager:
    """ Предоставляет интерфейс для работы с объектами лекции (Lecture) в базе данных """

    def __init__(self, from_attr: AttrNames = AttrNames.LECTURER):
        self._from_attr = from_attr.value

    @staticmethod
    def get_lecture_by_id(lecture_id: int) -> Lecture:
        """ Получает лекцию из базы данных. Выбрасывает исключение, если лекции не существует. """

        lecture = Lecture.objects.filter(pk=lecture_id).first()

        if not lecture:
            return lecture_responses.does_not_exist()
        return lecture


class ChatManager(LectureObjectManager):
    @staticmethod
    def get_chat_by_dates(dates: QuerySet[LectureRequest], creator: User, respondent: User) -> Chat:
        """ Возвращает объект Chat у которого даты dates, и собеседники creator и respondent """

        return Chat.objects.filter(
            lecture_requests__in=dates, users=creator).filter(
            users=respondent).first()

    @staticmethod
    def create_chat(lecture: Lecture) -> Chat:
        return Chat.objects.create(lecture=lecture)

    @staticmethod
    def add_responses(chat: Chat, responses: QuerySet[LectureRequest], save: bool = True) -> None:
        """ Добавляет даты responses в атрибут lecture_requests переданного объекта Chat """

        chat.lecture_requests.add(*responses)
        if save:
            chat.save()

    @staticmethod
    def add_users(chat: Chat, creator: User, respondent: User, save: bool = True) -> None:
        """ Добавляет даты responses в атрибут lecture_requests переданного объекта Chat """

        chat.users.add(creator, respondent)
        if save:
            chat.save()

    @staticmethod
    def create_message(chat: Chat, author: User, text: str) -> Message:
        return Message.objects.create(
            author=author,
            chat=chat,
            text=text
        )


class GetLectureManager(LectureObjectManager):
    """ Интерфейс для получения объектов из базы данных """

    def __init__(self, person: Person, from_attr: AttrNames, to_attr: AttrNames = None):
        super().__init__(from_attr=from_attr)
        self._person = person

        if to_attr is None:
            self._to_attr = from_attr.value
        else:
            self._to_attr = to_attr.value

    def get_person_lectures(self) -> QuerySet[Lecture]:
        """ Возвращает все лекции пользователя по выбранному аттрибуту (self.attr_name) """

        if not hasattr(self._person, self._from_attr):
            msg = 'У объекта {} нет аттрибута {}'.format(self._person, self._from_attr)
            raise AttributeError(msg)
        return getattr(self._person, self._from_attr).lectures.all()

    @staticmethod
    def get_latest_lecture_date(lecture: Lecture) -> datetime.datetime:
        """ Возвращает самую позднюю дату лекции """

        aggregate = lecture.lecture_requests.aggregate(latest=Max('event__datetime_start'))
        return aggregate.get('latest')

    def get_person_confirmed_lectures(self) -> list[Lecture]:
        """ Возвращает список подтвержденных лекций пользователя self._person (те, которые он создал) """

        if not hasattr(self._person, self._from_attr):
            raise AttributeError(f'У объекта {self._person} нет аттрибута {self._from_attr}')

        lecture_list = []

        lectures = getattr(self._person, self._from_attr).lectures.filter(
            lecture_requests__respondent_obj__confirmed=True,
            lecture_requests__event__datetime_start__gte=datetime.datetime.now())

        for own_lecture in lectures:
            if getattr(own_lecture, self._from_attr) and own_lecture not in lecture_list:
                lecture_list.append(own_lecture)

        return lecture_list

    def get_person_confirmed_responses(self) -> list[Lecture]:
        """ Возвращает список лекций на который откликнулся пользователь self._person """

        lecture_list = []

        respondents = self._person.respondent_obj.filter(
            confirmed=True,
            lecture_request__event__datetime_start__gte=datetime.datetime.now())

        for respondent in respondents:
            lecture = respondent.lecture_request.lecture
            if getattr(lecture, self._to_attr) and lecture not in lecture_list:
                lecture_list.append(lecture)

        return lecture_list


class DeleteLectureManager(LectureObjectManager):
    @staticmethod
    def delete(lecture: Lecture) -> int:
        """ Удаляет лекцию """

        id_ = lecture.pk
        lecture.delete()
        return id_


class LectureResponseManager(LectureObjectManager):
    @staticmethod
    def get_person_rejected_lecture_requests(person: Person, lecture: Lecture) -> QuerySet[LectureRequest]:
        """ Возвращает список дат лекции, на которые пользователь
         получил отклонение отклика хотябы на одну из дат лекции """

        return lecture.lecture_requests.filter(
            respondents=person, respondent_obj__rejected=True)

    @staticmethod
    def get_responses(lecture: Lecture, dates: list[datetime.datetime]) -> QuerySet[LectureRequest]:
        """ Возвращает все объекты LectureRequest переданной лекции с выбранными датами """

        responses = lecture.lecture_requests.filter(
            event__datetime_start__in=dates)

        if not responses:
            return lecture_responses.does_not_exist()
        return responses

    @staticmethod
    def add_respondent(person: Person, responses: QuerySet[LectureRequest]) -> None:
        """ Принимает даты лекции, на которые надо откликнуться пользователю (person) """

        for response_request in responses:
            response_request.respondents.add(person)
            response_request.save()
