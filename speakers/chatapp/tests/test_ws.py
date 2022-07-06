import json
from typing import TypedDict, Optional, Type, Union

from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.http import HttpRequest

from authapp.models import User
from chatapp.models import WsClient, Chat
from chatapp.routing import websocket_urlpatterns
from services.types import WsEventTypes
from services.api import service_response_to_lecture, service_cancel_response_to_lecture, \
    service_confirm_respondent_to_lecture
from workroomsapp.models import Lecturer, Lecture, Person, Customer
from workroomsapp.person.tests.base import SignUpTestCase, LecturerTestManager, CustomerTestManager, LectureTestManager


@database_sync_to_async
def get_first_object(obj: Union[Type[Lecturer], Type[Customer], Type[Person], Type[User]]):
    return obj.objects.first()


@database_sync_to_async
def get_person_from_obj(obj: Union[Type[Lecturer], Type[Customer]]):
    return obj.objects.first().person


@database_sync_to_async
def get_chat():
    return Chat.objects.prefetch_related('users').first()


@database_sync_to_async
def get_ws_client(user):
    return WsClient.objects.filter(user=user).first()


@database_sync_to_async
def get_lecture_first_date(lecture):
    return lecture.lecture_requests.first().event.datetime_start.strftime('%Y-%m-%dT%H:%M')


@database_sync_to_async
def get_user_from_lecture(lecture):
    return lecture.lecturer.person.user


async def websocket_connect():
    user = await get_first_object(User)
    route = f'ws/connect/{user.pk}'

    communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), route)
    connect, _ = await communicator.connect()
    return user, communicator


@database_sync_to_async
def create_lecture(request: HttpRequest):
    lecturer_manager = LecturerTestManager()
    customer_manager = CustomerTestManager()

    lecturer_manager.create_obj()
    customer_manager.create_obj()

    lecture_manager = LectureTestManager(Lecturer.objects.first())
    lecture_manager.create_obj()

    lecture = Lecture.objects.first()
    request.user = customer_manager._user  # откликается Customer
    return lecture


class NewRespondentEvent(TypedDict):
    type: WsEventTypes
    respondent_id: int
    id: int
    lecture_name: str
    lecture_svg: int
    need_read: bool
    talker_id: int
    talker_first_name: str
    talker_last_name: str
    talker_photo: str
    chat_confirm: Optional[bool]


class RemoveRespondentEvent(TypedDict):
    type: WsEventTypes
    id: int


class ChatMessageEvent(TypedDict):
    type: WsEventTypes
    author: int
    text: str
    chat_id: int
    confirm: Optional[bool]


class ConsumerTestCase(SignUpTestCase):
    async def test_connect(self):
        user = await get_first_object(User)
        route = f'ws/connect/{user.pk}'

        communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), route)
        connect, _ = await communicator.connect()
        self.assert_(connect, 'Не удалось установить WebSocket соединение')

        ws_client = await get_ws_client(user)
        self.assert_(ws_client, 'WsClient не был создан при подключении')

        await communicator.disconnect()
        ws_client_again = await get_ws_client(user)
        self.assert_(not ws_client_again, 'WsClient не был удален при завершении соединения')

    async def test_new_respondent(self):
        user, communicator = await websocket_connect()

        request = HttpRequest()
        lecture = await create_lecture(request)

        date = await get_lecture_first_date(lecture)
        await database_sync_to_async(service_response_to_lecture)(
            request,
            lecture_id=lecture.pk,
            dates=[date])

        await communicator.receive_from()  # set_online_users event
        new_respondent_event = await communicator.receive_from()
        new_respondent = json.loads(new_respondent_event)

        self.assertEqual(len(new_respondent), 11, msg='Неверное количество ключей в событии new_respondent')

    async def test_remove_respondent(self):
        user, communicator = await websocket_connect()

        request = HttpRequest()
        lecture = await create_lecture(request)

        date = await get_lecture_first_date(lecture)
        await database_sync_to_async(service_response_to_lecture)(
            request,
            lecture_id=lecture.pk,
            dates=[date],
            ws_active=False,  # не отправляем сообщение по вебсокету
        )

        await database_sync_to_async(service_cancel_response_to_lecture)(request, lecture.pk)

        await communicator.receive_from()  # set_online_users event
        remove_respondent_event = await communicator.receive_from()
        remove_respondent = json.loads(remove_respondent_event)

        self.assertEqual(len(remove_respondent), 2, msg='Неверное количество ключей в событии remove_respondent')

    async def test_send_chat_message(self):  # тест через подтверждение откликнувшегося пользователя
        user, communicator = await websocket_connect()

        request = HttpRequest()
        lecture: Lecture = await create_lecture(request)  # создатель лекции Lecturer

        date: str = await get_lecture_first_date(lecture)
        await database_sync_to_async(service_response_to_lecture)(
            request,
            lecture_id=lecture.pk,
            dates=[date],
            ws_active=False,  # не отправляем сообщение по вебсокету
        )
        respondent = await get_person_from_obj(Customer)  # берем откликнувшегося
        request2 = HttpRequest()
        request2.user = await get_user_from_lecture(lecture)  # помещаем создателя в объект запроса
        chat = await get_chat()
        await database_sync_to_async(service_confirm_respondent_to_lecture)(
            request2, chat.pk, respondent.pk)

        await communicator.receive_from()  # set_online_users event
        chat_message_event = await communicator.receive_from()
        chat_message = json.loads(chat_message_event)

        self.assertEqual(len(chat_message), 5, msg='Неверное количество ключей в событии chat_message')
