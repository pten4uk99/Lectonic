from authapp.models import User
from workroomsapp.lecture.services.db import AttrNames


class Service:
    """ Реализует бизнес логику проекта """

    object_manager = None

    def __init__(self, from_obj: User, from_attr: AttrNames = AttrNames.LECTURER):
        self.from_attr = from_attr
        self.from_obj = from_obj

        if self.object_manager is not None:
            self.object_manager = self.object_manager(from_attr)
