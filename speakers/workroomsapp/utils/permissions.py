from rest_framework.permissions import BasePermission
from workroomsapp.models import Person
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


class IsLecturer(BasePermission):
    """ Предоставляет доступ только лекторам. """

    def has_permission(self, request, view):
        try:
            pers = Person.objects.get(id = request.user.pk).is_lecturer
        except ObjectDoesNotExist:
            return Response(
                data={"status":"error",
                    "description": "NoProfile",
                    "user_msg":"Необходимо заполнить профиль и войти под учетной записью лектора"
                    },
                status=404
            )
        return bool(request.user and pers)


class IsProjectAdmin(BasePermission):
    """ Предоставляет доступ только админитраторам проекта. """

    def has_permission(self, request, view):
        try:
            pers = Person.objects.get(id = request.user.pk).is_project_admin
        except ObjectDoesNotExist:
            return Response(
                data={"status":"error",
                    "description": "NoProfile",
                    "user_msg":"Необходимо заполнить профиль и войти под учетной записью админитратора проекта"
                    },
                status=404
            )
        return bool(request.user and pers)


class IsCustomer(BasePermission):
    """ Предоставляет доступ только заказчикам. """

    def has_permission(self, request, view):
        try:
            pers = Person.objects.get(id = request.user.pk).is_customer
        except ObjectDoesNotExist:
            return Response(
                data={"status":"error",
                    "description": "NoProfile",
                    "user_msg":"Необходимо заполнить профиль и войти под учетной записью заказчика"
                    },
                status=404
            )
        return bool(request.user and pers)


class IsVerified(BasePermission):
    """ Предоставляет доступ только пользователям, у которых документы
    проверены модераторами. """

    def has_permission(self, request, view):
        try:
            pers = Person.objects.get(id = request.user.pk).is_verified
        except ObjectDoesNotExist:
            return Response(
                data={"status":"error",
                    "description": "NoProfile",
                    "user_msg":"Необходимо заполнить профиль и предоставить документы модераторам"
                    },
                status=404
            )
        return bool(request.user and pers)
