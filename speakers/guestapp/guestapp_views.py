from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from guestapp.guestapp_serializers import GuestLectureSerializer, GuestPersonSerializer
from workroomsapp.models import Lecture, Person
from guestapp.utils.guestapp_responses import *


class LecturesAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        if 'id' in request.GET:
            lec_id = request.GET['id']
            lecture = Lecture.objects.filter(id=lec_id).first()
            if not lecture:
                return lecture_does_not_exist()
            lec_data = GuestLectureSerializer(lecture)
            return success_response(lec_data.data)
        else:
            if 'closer' in request.GET:
                closer_count = request.GET['closer']
                if (closer_count.isdigit() and int(closer_count) > 0):
                    all_lecs = Lecture.objects.all().order_by('date')
                    if not all_lecs:
                        return have_no_lectures()
                    lectures = GuestLectureSerializer(all_lecs[:int(closer_count)], many=True)
                    return success_response(lectures.data)
                else:
                    return wrong_format()
            elif 'last' in request.GET:
                last_count = request.GET['last']
                if (last_count.isdigit() and int(last_count) > 0):
                    all_lecs = Lecture.objects.all().order_by('-sys_created_at')
                    if not all_lecs:
                        return have_no_lectures()
                    lectures = GuestLectureSerializer(all_lecs[:int(last_count)], many=True)
                    return success_response(lectures.data)
                else:
                    return wrong_format()
            else:
                all_lecs = Lecture.objects.all().order_by('-sys_created_at')
                if not all_lecs:
                    return have_no_lectures()
                lectures = GuestLectureSerializer(all_lecs, many=True)
                return success_response(lectures.data)


class LecturersAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        if 'id' in request.GET:
            lecturer_id = request.GET['id']
            lecturer = Person.objects.filter(id=lecturer_id, is_lecturer=True).first()
            if not lecturer:
                return lecturer_does_not_exist()
            lecturer_data = GuestPersonSerializer(lecturer)
            return success_response(lecturer_data.data)
        elif 'last' in request.GET:
            last_count = request.GET['last']
            if (last_count.isdigit() and int(last_count) > 0):
                all_lecturers = Person.objects.filter(is_lecturer=True).order_by('-sys_created_at')
                if not all_lecturers:
                    return have_no_lecturers()
                lecturers = GuestPersonSerializer(all_lecturers[:int(last_count)], many=True)
                return success_response(lecturers.data)
            else:
                return wrong_format()
        else:
            all_lecturers = Person.objects.filter(is_lecturer=True).order_by('-sys_created_at')
            if not all_lecturers:
                return have_no_lecturers()
            lecturers = GuestPersonSerializer(all_lecturers, many=True)
            return success_response(lecturers.data)
