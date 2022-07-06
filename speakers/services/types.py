from enum import Enum
from typing import NewType, NamedTuple

from authapp.models import User, Token

# Type Aliases
person_id = NewType('person_id', int)


# -------------------------------


class UserLogin(NamedTuple):
    user: User
    token: Token


class WsEventTypes(Enum):
    new_respondent = 'new_respondent'
    set_online_users = 'set_online_users'
    remove_respondent = 'remove_respondent'
    chat_message = 'chat_message'
    read_messages = 'read_messages'
    read_reject_chat = 'read_reject_chat'


class WsGroups(Enum):
    common = 'common'


class AttrNames(Enum):
    LECTURER = 'lecturer'
    CUSTOMER = 'customer'
