from rest_framework.response import Response
from rest_framework.views import APIView
from workroomsapp.utils.permissions import IsLecturer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.core.exceptions import ObjectDoesNotExist
from workroomsapp.models import *
from workroomsapp.serializers.lector_serializers import *

class LectorLecturesAPIView(APIView):
    permission_classes = [IsAuthenticated&(IsLecturer|IsAdminUser)]
    def post(self, request):
        lec_add_serializer = LectureSerializer(data=request.data,
                                                context=request,
                                                )
        lec_add_serializer.is_valid()
        if lec_add_serializer.errors:
            return Response(
            data={"status":"error",
                "description": "ValidationError",
                "user_msg": lec_add_serializer.errors,
            },
            status=400
        )
        lec_add_serializer.save()
        return Response(
            data={"status":"ok"},
            status=201
        )
    def get(self, request):
        if 'id' in request.GET:
            lec_id = request.GET['id']
            lecture = Lecture.objects.filter(id=lec_id).first()
            if not lecture:
                return Response(
                    data={"status":"warning",
                        "description": "NoSuchLecture",
                        "user_msg":"Нет лекции с таким id"
                        },
                    status=204
                )
            lec_data = LectureSerializer(lecture)
            return Response(
                data={"status":"ok",
                    "lecture":lec_data.data
                    },
                status=200
            )
        else:
            try:
                lecturer = User.objects.get(id=request.user.pk)
                comms = lecturer.lectures.all()
                count = len(comms)
            except ObjectDoesNotExist:
                return Response(
                    data={"status":"warning",
                        "description": "NoLecturesFound",
                        "user_msg":"У Вас не добавлено ни одной лекции"
                        },
                    status=204
                )
            lectures = LectorLecturesSerializer(comms, many = True)
            return Response(
                data={"status":"ok",
                    "count":count,
                    "lectures":lectures.data
                    },
                status=200
            )

    def patch(self,request):
        if 'id' in request.data:
            lec_id = request.data['id']
            lecture = Lecture.objects.filter(id=lec_id).first()
            if not lecture:
                return Response(
                    data={"status":"warning",
                        "description": "NoSuchLecture",
                        "user_msg":"Нет лекции с таким id"
                        },
                    status=204
                )
            lec_data = LectureSerializer(lecture, data = request.data, partial=True)
            lec_data.is_valid()
            if lec_data.errors:
                return Response(
                    data={"status":"error",
                        "description": "ValidationError",
                        "user_msg": lec_data.errors,
                    },
                    status=400
                )
            lec_data.save()
            return Response(
                data={"status":"ok"},
                status=200
            )
        else:
            return Response(
                    data={"status":"error",
                        "description": "NoLectureId",
                        "user_msg":"Не указан id лекции"
                        },
                    status=400
                )

    def delete(self,request):
        if 'id' in request.data:
            lec_id = request.data['id']
            lecture = Lecture.objects.filter(id=lec_id).first()
            if not lecture:
                return Response(
                    data={"status":"warning",
                        "description": "NoSuchLecture",
                        "user_msg":"Нет лекции с таким id"
                        },
                    status=204
                )
            lecture.delete()
            return Response(
                data={"status":"ok"},
                status=200
            )
        else:
            return Response(
                    data={"status":"error",
                        "description": "NoLectureId",
                        "user_msg":"Не указан id лекции"
                        },
                    status=400
                )

class DeleteMultipleLecture(APIView):
    permission_classes = [IsAuthenticated&(IsLecturer|IsAdminUser)]
    def delete(self,request):
        if 'id_list' in request.data:
            lec_ids = dict(request.data)['id_list']
            errors = {}
            success = {}
            for id in lec_ids:
                try:
                    int(id)
                except ValueError:
                    errors[id] = 'NotANumber'
                    continue
                try:
                    lecture = Lecture.objects.get(id=id)
                except ObjectDoesNotExist:
                    errors[id] = 'NoSuchLectureId'
                    continue
                lecture.delete()
                success[id] = 'Deleted'
            if not errors:
                return Response(
                    data={"status":"ok",
                        "description": "AllLecturesDeleted",
                        "user_msg":success
                        },
                    status=200
                )
            elif not success:
                return Response(
                    data={"status":"warning",
                        "description": "NoDeletedLectures",
                        "user_msg":errors
                        },
                    status=204
                )
            else:
                return Response(
                    data={"status":"warning",
                        "description": "NotAllLecturesDeleted",
                        "user_msg": {**errors, **success}
                        },
                    status=204
                )
        else:
            return Response(
                    data={"status":"error",
                        "description": "NoLectureIdList",
                        "user_msg":"Не указан список id лекций для удаления"
                        },
                    status=400
                )
