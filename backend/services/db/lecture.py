import datetime
from typing import Type, TypeVar

from django.db.models import QuerySet, Max

from authapp.models import User
from chatapp.models import Chat, Message, WsClient
from config.db import ObjectManager
from services.types import AttrNames
from workroomsapp.lecture import lecture_responses
from workroomsapp.models import Person, Lecture, LectureRequest

Model = TypeVar('Model')


class LectureObjectManager(ObjectManager):
    """ Предоставляет интерфейс для работы с объектами лекции (Lecture) в базе данных """

    def __init__(self, from_attr: AttrNames = AttrNames.LECTURER):
        self.from_attr = from_attr.value

    @staticmethod
    def get_lecture_by_id(lecture_id: int) -> Lecture:
        """ Получает лекцию из базы данных. Выбрасывает исключение, если лекции не существует. """

        lecture = Lecture.objects.filter(pk=lecture_id).first()

        if not lecture:
            return lecture_responses.does_not_exist()
        return lecture

    @staticmethod
    def get_object_by_id(obj: Type[Model], id_: int) -> Model:
        return obj.objects.filter(pk=id_).first()

    @staticmethod
    def get_lecture_requests_by_chat(chat: Chat) -> QuerySet[LectureRequest]:
        return chat.lecture_requests.all()


class ChatManager(LectureObjectManager):
    @staticmethod
    def get_chat_by_dates(dates: QuerySet[LectureRequest], creator: User, respondent: User) -> Chat:
        """ Возвращает объект Chat у которого даты dates, и собеседники creator и respondent """

        return Chat.objects.filter(
            lecture_requests__in=dates, users=creator).filter(
            users=respondent).first()

    @staticmethod
    def get_ws_client(channel_name=None, user_id=None):
        if user_id is not None:
            client = WsClient.objects.filter(user_id=user_id).first()
        elif channel_name is not None:
            client = WsClient.objects.filter(channel_name=channel_name).first()
        else:
            raise AttributeError('В функцию должен быть передан хотя бы один аргумент')
        return client

    @staticmethod
    def get_lecture_request_chats_with_exclude(lecture_request: LectureRequest,
                                               exclude_user: User) -> QuerySet[Chat]:
        return lecture_request.chat_list.exclude(users=exclude_user)

    @staticmethod
    def get_user_from_chat(chat: Chat, exclude_user: User) -> User:
        return chat.users.exclude(pk=exclude_user.pk).first()

    @staticmethod
    def count_chat_lecture_requests(chat: Chat) -> int:
        return chat.lecture_requests.all().count()

    @staticmethod
    def remove_lecture_request_from_chat(chat: Chat, lecture_request: LectureRequest) -> None:
        chat.lecture_requests.remove(lecture_request)
        chat.save()

    @staticmethod
    def create_chat(lecture: Lecture) -> Chat:
        return Chat.objects.create(lecture=lecture)

    @staticmethod
    def delete_chat(chat: Chat) -> None:
        chat.delete()

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
    def create_message(chat: Chat, author: User, text: str = '', system_text: str = '') -> Message:
        return Message.objects.create(
            author=author,
            chat=chat,
            text=text,
            system_text=system_text,
        )

    @staticmethod
    def read_message(message: Message) -> None:
        message.need_read = False
        message.save()

    @staticmethod
    def set_chat_confirm(chat: Chat, confirm: bool) -> None:
        chat.confirm = confirm
        chat.save()

    @staticmethod
    def delete_first_message(messages: QuerySet[Message]) -> None:
        messages.first().delete()

    @staticmethod
    def count_messages(messages: QuerySet[Message]) -> int:
        return messages.count()

    @staticmethod
    def get_messages_by_chat(chat_id: int) -> QuerySet[Message]:
        return Message.objects.filter(chat_id=chat_id)

    @staticmethod
    def exclude_user_in_messages(messages: QuerySet[Message], user_id: int) -> QuerySet[Message]:
        return messages.exclude(author_id=user_id)


class GetLectureManager(LectureObjectManager):
    """ Интерфейс для получения объектов из базы данных """

    def __init__(self, from_obj: User, from_attr: AttrNames, to_attr: AttrNames = None):
        super().__init__(from_attr=from_attr)
        self._from_obj = from_obj

        if to_attr is None:
            self._to_attr = from_attr.value
        else:
            self._to_attr = to_attr.value

    def get_person_lectures(self) -> QuerySet[Lecture]:
        """ Возвращает все лекции пользователя по выбранному аттрибуту (self.from_attr) """

        if not hasattr(self._from_obj.person, self.from_attr):
            msg = 'У объекта {} нет аттрибута {}'.format(self._from_obj.person, self.from_attr)
            raise AttributeError(msg)
        return getattr(self._from_obj.person, self.from_attr).lectures.all()

    @staticmethod
    def get_confirmed_lecture_request(lecture: Lecture, respondent: Person) -> LectureRequest:
        return lecture.lecture_requests.filter(
            respondent_obj__confirmed=True, respondent_obj__person=respondent).first()


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
        """ Возвращает список дат лекции, хотя бы на одну из которых
        пользователь получил отклонение отклика """

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

    @staticmethod
    def get_chat_from_lecture(lecture: Lecture, respondent: User) -> Chat:
        chat = Chat.objects.filter(lecture=lecture, users=respondent).prefetch_related('users').first()
        return chat

    @staticmethod
    def get_confirmed_lecture_requests_in_chat(lecture: Lecture, chat: Chat) -> QuerySet[LectureRequest]:
        """ Возвращает список подтвержденных дат лекции в текущем чате """

        return lecture.lecture_requests.filter(
            chat_list=chat, respondent_obj__confirmed=True)

    @staticmethod
    def get_lecture_request_respondents(lecture_request: LectureRequest,
                                        respondent_id: int) -> QuerySet[Person]:
        return lecture_request.respondents.exclude(pk=respondent_id)

    @staticmethod
    def remove_lecture_request_respondent(lecture_request: LectureRequest, respondent: Person) -> None:
        lecture_request.respondents.remove(respondent)
        lecture_request.save()

    @staticmethod
    def confirm_respondent(lecture_request: LectureRequest, respondent: Person) -> None:
        lecture_respondent = lecture_request.respondent_obj.get(person=respondent)
        lecture_respondent.confirmed = True
        lecture_respondent.save()

    @staticmethod
    def reject_respondent(lecture_request: LectureRequest, respondent: Person) -> None:
        lecture_respondent = lecture_request.respondent_obj.get(person=respondent)
        lecture_respondent.rejected = True
        lecture_respondent.save()
