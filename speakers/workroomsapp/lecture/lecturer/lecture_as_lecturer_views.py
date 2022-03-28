from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.lecturer.lecture_as_lecturer_serializers import *
from workroomsapp.models import Respondent, CustomerLectureRequest
from workroomsapp.utils import workroomsapp_permissions


class LectureAsLecturerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer]

    @swagger_auto_schema(**lecture_docs.LectureAsLecturerCreateDoc)
    def post(self, request):
        serializer = LectureCreateAsLecturerSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_created()

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        customer_lectures = CustomerLectureRequest.objects.order_by(
            'lecture_request__events__datetime_start').all()

        serializer = LectureAsLecturerGetSerializer(customer_lectures, many=True)
        return lecture_responses.success_get_lectures(serializer.data)




class LectureResponseAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecture_id = request.GET.get('lecture')

        if not lecture_id:
            return lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=lecture_id).first()

        if not lecture:
            return lecture_responses.lecture_does_not_exist()

        if not hasattr(lecture.lecture_request, 'lecturer_lecture_request'):
            if not hasattr(request.user.person, 'customer'):
                return lecture_responses.lecturer_forbidden()

        if not hasattr(lecture.lecture_request, 'customer_lecture_request'):
            if not hasattr(request.user.person, 'lecturer'):
                return lecture_responses.customer_forbidden()

        respondent = Respondent.objects.create(person=request.user.person)
        lecture_request = lecture.lecture_request

        if not lecture_request.respondents.filter(person=request.user.person).first():
            lecture_request.respondents.add(respondent)
            lecture_request.save()
            return lecture_responses.success_response()
        else:
            lecture_request.respondents.remove(respondent)
            lecture_request.save()
            return lecture_responses.success_cancel()


class LectureConfirmRespondentAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecture_id = request.GET.get('lecture')
        respondent_id = request.GET.get('respondent')

        if not lecture_id or not respondent_id:
            return lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=lecture_id).first()

        if not lecture:
            return lecture_responses.lecture_does_not_exist()

        lecturer_lecture = None
        customer_lecture = None
        if request.user.person.is_lecturer:
            lecturer_lecture = request.user.lecturer.lecturer_lecture_requests.filter(
                lecture_request__lecture=lecture).first()
        elif request.user.person.is_customer:
            customer_lecture = request.user.customer.customer_lecture_requests.filter(
                lecture_request__lecture=lecture).first()

        if not lecturer_lecture and not customer_lecture:
            return lecture_responses.not_a_creator()

        respondent = lecture.lecture_request.respondents.filter(pk=respondent_id)

        if not respondent:
            return lecture_responses.not_a_respondent()

        if respondent.confirmed:
            respondent.confirmed = False
            lecture.status = False
            lecture.save()
            respondent.save()
            return lecture_responses.success_denied()
        else:
            respondent.confirmed = True
            lecture.status = True
            lecture.save()
            respondent.save()
            return lecture_responses.success_confirm()
