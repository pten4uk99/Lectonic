from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.core.exceptions import ObjectDoesNotExist
from workroomsapp.models import *
from workroomsapp.serializers.guest_serializers import *


class LecturesAPIView(APIView):
    def get(self,request):
        if 'id' in request.GET:
            lec_id = request.GET['id']
            lecture = Lecture.objects.filter(id=lec_id).first()
            if not lecture:
                return Response(
                    data={"status":"error",
                        "description": "NoSuchLecture",
                        "user_msg":"Нет лекции с таким id"
                        },
                    status=204
                )
            lec_data = GuestLectureSerializer(lecture)
            return Response(
                data={"status":"ok",
                    "lecture":lec_data.data
                    },
                status=200
            )
        else:
            try:
                all_lecs = Lecture.objects.all()
            except ObjectDoesNotExist:
                return Response(
                    data={"status":"error",
                        "description": "NoLecturesFound",
                        "user_msg":"В БД не добавлено ни одной лекции"
                        },
                    status=204
                )
            lectures = GuestLectureSerializer(all_lecs, many = True)
            return Response(
                data={"status":"ok",
                    "lectures":lectures.data
                    },
                status=200
            )