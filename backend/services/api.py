from abc import abstractmethod
from typing import Type

from rest_framework.serializers import Serializer

from authapp.models import User
from chatapp.chatapp_serializers import ChatMessageListSerializer
from services import AttrNames
from services.authapp import UserCreateService
from services.chat.chatapp import ChatMessageService
from services.lecture import LectureResponseService, LectureCancelResponseService, \
    LectureConfirmRespondentService, LectureRejectRespondentService, LectureDeleteService
from services.types import UserLogin, user_id_type


# Тут описаны методы взаимодействия с представлениями

class BaseLectureAPI:
    def __init__(self, from_obj: User, from_attr: AttrNames):
        self.from_obj = from_obj
        self.from_attr = from_attr
        self.to_attr = AttrNames.LECTURER if self.from_attr == AttrNames.CUSTOMER else AttrNames.CUSTOMER


class SerializerAPI(BaseLectureAPI):
    serializer_class: Type[Serializer]

    @abstractmethod
    def init_serializer(self) -> Serializer:
        """ Создает объект self.serializer_class """

    def serialize(self) -> Serializer:
        """ Метод, который должен возвращать объект сериализатора с готовыми данными """
        return self.init_serializer()


class ChatMessageAPI(SerializerAPI):
    serializer_class = ChatMessageListSerializer
    service = ChatMessageService

    def __init__(self, from_obj: User, chat_id: int, from_attr: AttrNames = AttrNames.LECTURER):
        super().__init__(from_obj=from_obj, from_attr=from_attr)
        self.service = self.service(from_obj=from_obj, chat_id=chat_id, from_attr=from_attr)

    def init_serializer(self) -> Serializer:
        return self.serializer_class(
            [self.service.chat], many=True, context={'user': self.service.from_obj})

    def serialize(self) -> Serializer:
        self.service.setup()
        return super().serialize()


# ------------------Функции для использования непосредственно в представлениях-------------------
# ---------------------------------------------------------------------------------------
def service_delete_lecture_by_id(from_obj: User, lecture_id: int) -> None:
    service = LectureDeleteService(from_obj=from_obj, lecture_id=lecture_id)
    service.setup()


def service_response_to_lecture(from_obj: User, lecture_id: int, dates: list[str], ws_active: bool = True):
    service = LectureResponseService(
        from_obj=from_obj, lecture_id=lecture_id, response_dates=dates, ws_active=ws_active)
    service.setup()


def service_cancel_response_to_lecture(from_obj: User, lecture_id: int):
    service = LectureCancelResponseService(from_obj=from_obj, lecture_id=lecture_id)
    service.setup()


def service_confirm_respondent_to_lecture(from_obj: User, chat_id: int, respondent_id: user_id_type):
    service = LectureConfirmRespondentService(from_obj=from_obj, chat_id=chat_id, respondent_id=respondent_id)
    service.setup()


def service_reject_respondent_to_lecture(from_obj: User, chat_id: int, respondent_id: user_id_type):
    service = LectureRejectRespondentService(from_obj=from_obj, chat_id=chat_id, respondent_id=respondent_id)
    service.setup()


def serialize_chat_message_list(from_obj: User, chat_id: int):
    return ChatMessageAPI(from_obj=from_obj, chat_id=chat_id).serialize()


def user_signup_service(data: dict, pk: int = None) -> tuple[UserLogin, Serializer]:
    service = UserCreateService(data=data, pk=pk)
    return service.setup(), service.serializer
