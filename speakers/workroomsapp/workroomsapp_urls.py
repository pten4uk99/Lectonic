from django.urls import path

from workroomsapp.calendar.customer.customer_calendar_views import *
from workroomsapp.calendar.lecturer.lecturer_calendar_views import *
from workroomsapp.lecture.customer.lecture_as_customer_views import *
from workroomsapp.lecture.lecturer.lecture_as_lecturer_views import *
from workroomsapp.lecturer.lecturer_views import *
from workroomsapp.customer.customer_views import *
from workroomsapp.person.person_views import *


urlpatterns = [
    path('profile/', PersonAPIView.as_view(), name='profile'),
    path('profile/document_photos/', DocumentImageAPIVIew.as_view(), name='document_images'),
    path('city/', CityGetAPIView.as_view(), name='city'),
    path('domain/', DomainGetAPIView.as_view(), name='domain'),

    path('lecture/response/', LectureResponseAPIView.as_view(), name='lecture_response'),
    path('lecture/response/confirm/', LectureToggleConfirmRespondentAPIView.as_view(), name='lecture_confirm'),
    path('lecture/as_lecturer/', LectureAsLecturerAPIView.as_view(), name='lecture_as_lecturer'),
    path('lecture/as_customer/', LectureAsCustomerAPIView.as_view(), name='lecture_as_customer'),

    path('calendar/lecturer/', LecturerCalendarAPIView.as_view(), name='lecturer_calendar'),
    path('calendar/customer/', CustomerCalendarAPIView.as_view(), name='customer_calendar'),

    path('lecturer/', LecturerCreateAPIView.as_view(), name='lecturer'),
    path('lecturer/diploma_photos/', DiplomaImageAPIView.as_view(), name='diploma_images'),

    path('customer/', CustomerAPIView.as_view(), name='customer'),
]
