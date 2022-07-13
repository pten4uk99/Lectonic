from enum import Enum
from typing import NewType, NamedTuple, Literal, TypedDict, Optional

from authapp.models import User, Token

# Type Aliases

user_id_type = NewType('user_id_type', int)
person_id_type = NewType('person_id_type', int)


# -------------------------------


class UserLogin(NamedTuple):
    user: User
    token: Token


class WsGroups(Enum):
    common = 'common'


class AttrNames(Enum):
    LECTURER = 'lecturer'
    CUSTOMER = 'customer'


# WsEvents----------------------------

class WsEventTypes(Enum):
    new_respondent = 'new_respondent'
    set_online_users = 'set_online_users'
    remove_respondent = 'remove_respondent'
    chat_message = 'chat_message'
    read_messages = 'read_messages'
    read_reject_chat = 'read_reject_chat'


class SetOnlineUsersEventType(TypedDict):
    type: Literal[WsEventTypes.set_online_users]
    users: list[int]


class NewRespondentEventType(TypedDict):
    type: Literal[WsEventTypes.new_respondent]
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


class RemoveRespondentEventType(TypedDict):
    type: Literal[WsEventTypes.remove_respondent]
    id: int


class ChatMessageEventType(TypedDict):
    type: Literal[WsEventTypes.chat_message]
    author: int
    text: str
    chat_id: int
    confirm: Optional[bool]
    need_read: bool


class ReadMessagesEventType(TypedDict):
    type: Literal[WsEventTypes.read_messages]
    chat_id: int


class ReadRejectChatEventType(TypedDict):
    type: Literal[WsEventTypes.read_reject_chat]
    chat_id: int

# ----------------------------------------------
