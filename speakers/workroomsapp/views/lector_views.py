from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist
from workroomsapp.models import *
from workroomsapp.serializers.lector_serializers import *

class AddLecture(APIView):
    def post(self, request):
        if (request.user.is_authenticated or request.user.is_staff):
            try:
                user = Person.objects.get(id = request.user.pk)
            except ObjectDoesNotExist:
                return Response(
                    data={"status":"error","description": "NoProfile","user_msg":"Необходимо заполнить профиль"},
                    status=404
                )
            if user.isLecturer():
                pass
                # lec_add_serializer = LectureSerializer(data=request.data)
                # lec_add_serializer.is_valid() # TODO обработать ошибки
                # lec = lec_add_serializer.save() # Записываем лекцию в таблицу
                # Lecture.lecturers.add(user_id=User.objects.get(id = request.user.pk), lecture_id=lec) # Записываем связь лектора и лекции в бд
                # return Response(
                #     data={"status":"ok"},
                #     status=200
                # )
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

class GetLectorLectures(APIView):
    def get(self, request):
        if (request.user.is_authenticated or request.user.is_staff):
            try:
                user = Person.objects.get(id = request.user.pk)
            except ObjectDoesNotExist:
                return Response(
                    data={"status":"error","description": "NoProfile","user_msg":"Необходимо заполнить профиль"},
                    status=404
                )
            if user.isLecturer():
                # try:
                #     comms = Lecture_Lecturer.objects.filter(userId__id = request.user.pk)
                #     count = len(comms)
                # except ObjectDoesNotExist:
                #     return Response(
                #         data={"status":"error","description": "NoLecturesFound","user_msg":"У Вас не добавлено ни одной лекции"},
                #         status=404
                #     )
                # lectures = LectorLecturesCommunicationSerializer(comms, many = True)
                return Response(
                    data={"status":"ok",
                        # "count":count,
                        # "lectures":lectures.data
                        },
                    status=200
                )
            else:
                return Response(
                    data={"status":"error","description": "WrongAuthorization","user_msg":"Только лектор может посмотреть свои лекции"},
                    status=403
                )
        else:
            return Response(
                data={"status":"error","description": "Unauthorized","user_msg":"Требуется авторизация"},
                status=401
            )

class GetLecture(APIView):
    def get(self, request):
        if (request.user.is_authenticated or request.user.is_staff):
            try:
                user = Person.objects.get(id = request.user.pk)
            except ObjectDoesNotExist:
                return Response(
                    data={"status":"error","description": "NoProfile","user_msg":"Необходимо заполнить профиль"},
                    status=404
                )
            if user.isLecturer():
                if 'id' in request.GET:
                    lec_id = request.GET['id']
                    try:
                        lecture = Lecture.objects.get(id=lec_id)
                    except ObjectDoesNotExist:
                        return Response(
                            data={"status":"error","description": "NoSuchLecture","user_msg":"Нет лекции с таким id"},
                            status=404
                        )
                    lec_data = LectureSerializer(lecture)
                    return Response(
                        data={"status":"ok",
                            "lecture":lec_data.data
                            },
                        status=200
                    )
                else:
                    return Response(
                        data={"status":"error","description": "SyntaxError","user_msg":"Необходимо указать параметр id в get-запросе"},
                        status=404
                    )
            else:
                return Response(
                    data={"status":"error","description": "WrongAuthorization","user_msg":"Только лектор может посмотреть свои лекции"},
                    status=403
                )
        else:
            return Response(
                data={"status":"error","description": "Unauthorized","user_msg":"Требуется авторизация"},
                status=401
            )

class DeleteLecture(APIView):
    pass

class ModifyLecture(APIView):
    pass