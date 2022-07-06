from rest_framework.serializers import Serializer

from authapp.authapp_serializers import UserCreateSerializer
from authapp.models import User
from services.types import UserLogin


class UserCreateService:
    """
    Сервис реализующий логику по созданию пользователя в базе данных.

    Вызов метода setup() включает в себя все необходимые действия для успешного
    создания пользователя.
    """

    serializer_class = UserCreateSerializer

    def __init__(self, data: dict, pk: int = None):
        self.pk = pk
        self.data = data
        self.serializer = self._init_serializer()

    def _init_serializer(self) -> Serializer:
        """ Создает объект сериализатора и проверяет self.data """

        serializer = self.serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _save_model(self) -> User:
        """ Проверяет передан ли self.pk и сохраняет объект в БД """

        if self.pk is not None:
            return self.serializer.save(pk=self.pk)

        return self.serializer.save()

    @staticmethod
    def _login_user(user: User) -> UserLogin:
        user, token = user.login()
        return UserLogin(user=user, token=token)

    def setup(self) -> UserLogin:
        user = self._save_model()
        return self._login_user(user)
