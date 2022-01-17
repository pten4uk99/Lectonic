from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist
from workroomsapp.models import *

class AddLecture(APIView):
    def post(self, request):
        if (request.user.is_authenticated or request.user.is_staff):
            try:
                user = Person.objects.get(id = request.user.pk)
            except ObjectDoesNotExist:
                return Response(
                    data={"status":"error","description": "NoProfile","user_msg":"Необходимо заполнить профиль"},
                    status=500
                )
            if user.isLecturer():
                print(user)
                return Response(
                    data={"status":"ok"},
                    status=200
                )
            else:
                return Response(
                    data={"status":"error","description": "WrongAuthorization","user_msg":"Только лекторы могут добавлять лекции"},
                    status=403
                )
        else:
            return Response(
                data={"status":"error","description": "Unauthorized","user_msg":"Требуется авторизация"},
                status=401
            )