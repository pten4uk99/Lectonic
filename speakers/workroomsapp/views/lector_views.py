from rest_framework.response import Response
from rest_framework.views import APIView
from workroomsapp.utils.workroomsapp_permissions import IsLecturer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from workroomsapp.models import *
from workroomsapp.serializers.lector_serializers import *
from workroomsapp.utils.responses.lector_responses import *
from drf_yasg.utils import swagger_auto_schema
from workroomsapp.docs.lector_docs import GetLectorLecturesDescribe


def is_owner(lecture, user):
    '''Функция проверки находится-ли user в списке лекторов лекции lecture'''
    if user.is_superuser or user.is_staff:
        return True
    return user in lecture.lecturers.all()


class LectorLecturesAPIView(APIView):

    permission_classes = [IsAuthenticated & ( IsAdminUser | IsLecturer )]
    def post(self, request):
        lec_add_serializer = LectureSerializer(
            data=request.data,
            context=request,
        )
        lec_add_serializer.is_valid()

        if lec_add_serializer.errors:
            return validation_error(lec_add_serializer.errors)
        lec_add_serializer.save()
        return created(lec_add_serializer.validated_data)

    @swagger_auto_schema(**GetLectorLecturesDescribe)
    def get(self, request):
        if 'id' in request.GET:
            lec_id = request.GET['id']
            lecture = Lecture.objects.filter(id=lec_id, is_active = True).first()
            if not lecture:
                return lecture_does_not_exist()
            lec_data = LectureSerializer(lecture)
            return success_response(lec_data.data)
        else:
            lecturer = User.objects.get(id=request.user.pk)
            comms = lecturer.lectures.filter(is_active=True)
            if not comms:
                return have_no_lectures()
            lectures = LectorLecturesSerializer(comms, many=True)
            return success_response(lectures.data)

    def patch(self, request):
        if 'id' in request.data:
            lec_id = request.data['id']
            lecture = Lecture.objects.filter(id=lec_id, is_active = True).first()
            if not lecture:
                return lecture_does_not_exist()
            if is_owner(lecture, request.user):
                lec_data = LectureSerializer(lecture, data=request.data, partial=True)
                lec_data.is_valid()
                if lec_data.errors:
                    return validation_error(lec_data.errors)
                lec_data.save()
                return success_response(lec_data.validated_data)
            else: 
                return not_owner()
        else:
            return wrong_format()

    def delete(self, request):
        if 'id' in request.data:
            lec_id = request.data['id']
            lecture = Lecture.objects.filter(id=lec_id).first()
            if not lecture:
                return lecture_does_not_exist()
            if is_owner(lecture, request.user):
                lecture.delete()
                return success_response(data=None)
            else:
                return not_owner()
        else:
            return wrong_format()


class ArchiveLecture(APIView):
    permission_classes = [IsAuthenticated & ( IsAdminUser | IsLecturer )]
    def patch(self, request):
        if (len(request.data) != 1 or (('id' not in request.data) and ('id_list' not in request.data))):
            return wrong_format()
        else:
            if 'id' in request.data:
                lec_id = request.data['id']
                lecture = Lecture.objects.filter(id=lec_id, is_active=True).first()
                if not lecture:
                    return lecture_does_not_exist()
                if is_owner(lecture, request.user):
                    lecture.is_active = False
                    lecture.save()
                else:
                    return not_owner()
                return success_response(data=None)
            else:
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
                        lecture = Lecture.objects.get(id=id, is_active=True)
                    except ObjectDoesNotExist:
                        errors[id] = 'NoSuchLectureId'
                        continue
                    if is_owner(lecture, request.user):
                        lecture.is_active = False
                        lecture.save()
                        success[id] = 'Archived'
                    else:
                        errors[id] = 'Have no permissions'
                if not errors:
                    return success_response(success)
                elif not success:
                    return operation_report(errors)
                else:
                    return operation_report({**errors, **success})