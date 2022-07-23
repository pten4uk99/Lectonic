import json
from typing import Type, Union

from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator

from authapp.models import User
from chatapp.models import WsClient, Chat
from chatapp.routing import websocket_urlpatterns
from services.api import service_response_to_lecture, service_cancel_response_to_lecture, \
    service_confirm_respondent_to_lecture, serialize_chat_message_list
from workroomsapp.models import Lecturer, Lecture, Person, Customer
from workroomsapp.tests.base import SignUpTestCase
from workroomsapp.tests.managers import LecturerTestManager, CustomerTestManager, LectureTestManager


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
def create_lecture():
    lecturer_manager = LecturerTestManager()
    customer_manager = CustomerTestManager()

    lecturer_manager.create_obj()
    customer_manager.create_obj()

    lecture_manager = LectureTestManager(Lecturer.objects.first())
    lecture_manager.create_obj()

    lecture = Lecture.objects.first()
    respondent = customer_manager._user  # откликается Customer
    return lecture, respondent


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
        await communicator.disconnect()

    async def test_new_respondent(self):
        user, communicator = await websocket_connect()

        lecture, user = await create_lecture()

        date = await get_lecture_first_date(lecture)
        await database_sync_to_async(service_response_to_lecture)(
            user,
            lecture_id=lecture.pk,
            dates=[date])

        await communicator.receive_from()  # set_online_users event
        new_respondent_event = await communicator.receive_from()
        new_respondent = json.loads(new_respondent_event)

        self.assertEqual(len(new_respondent), 11, msg='Неверное количество ключей в событии new_respondent')
        await communicator.disconnect()

    async def test_remove_respondent(self):
        user, communicator = await websocket_connect()
        lecture, respondent = await create_lecture()

        date = await get_lecture_first_date(lecture)
        await database_sync_to_async(service_response_to_lecture)(
            respondent,
            lecture_id=lecture.pk,
            dates=[date],
            ws_active=False)

        await database_sync_to_async(service_cancel_response_to_lecture)(respondent, lecture.pk)

        await communicator.receive_from()  # set_online_users event
        remove_respondent_event = await communicator.receive_from()
        remove_respondent = json.loads(remove_respondent_event)

        self.assertEqual(len(remove_respondent), 2, msg='Неверное количество ключей в событии remove_respondent')
        await communicator.disconnect()

    async def test_send_chat_message(self):  # тест через подтверждение откликнувшегося пользователя
        user, communicator = await websocket_connect()

        lecture, respondent_user = await create_lecture()

        date = await get_lecture_first_date(lecture)
        await database_sync_to_async(service_response_to_lecture)(
            respondent_user,
            lecture_id=lecture.pk,
            dates=[date],
            ws_active=False)

        creator: User = await get_user_from_lecture(lecture)  # помещаем создателя в объект запроса
        chat = await get_chat()
        await database_sync_to_async(service_confirm_respondent_to_lecture)(
            creator, chat.pk, respondent_user.pk)

        await communicator.receive_from()  # set_online_users event
        chat_message_event = await communicator.receive_from()
        chat_message = json.loads(chat_message_event)

        self.assertEqual(len(chat_message), 5, msg='Неверное количество ключей в событии chat_message')
        await communicator.disconnect()

    async def test_read_messages(self):  # тест через подтверждение откликнувшегося пользователя
        user, communicator = await websocket_connect()
        lecture, respondent = await create_lecture()

        date = await get_lecture_first_date(lecture)
        await database_sync_to_async(service_response_to_lecture)(
            respondent,
            lecture_id=lecture.pk,
            dates=[date],
            ws_active=False)

        creator: User = await get_user_from_lecture(lecture)  # помещаем создателя в объект запроса
        chat = await get_chat()
        await database_sync_to_async(serialize_chat_message_list)(creator, chat.pk)

        await communicator.receive_from()  # set_online_users event
        read_messages_event = await communicator.receive_from()
        read_messages = json.loads(read_messages_event)

        self.assertEqual(
            len(read_messages), 2,
            msg='Неверное количество ключей в событии read_messages\n'
                f'{read_messages}')
        await communicator.disconnect()
