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

    path('lecture/<int:pk>/', LectureDetailAPIView.as_view(), name='lecture_detail'),
    path('lecture/response/', LectureResponseAPIView.as_view(), name='lecture_response'),
    path('lecture/response/confirm/', LectureToggleConfirmRespondentAPIView.as_view(), name='lecture_confirm'),
    path('lecture/as_lecturer/', LectureAsLecturerAPIView.as_view(), name='lecture_as_lecturer'),
    path('lecture/as_lecturer/history/',
         LecturerLecturesHistoryGetAPIView.as_view(),
         name='lecture_as_lecturer_history'),
    path('lecture/as_customer/', LectureAsCustomerAPIView.as_view(), name='lecture_as_customer'),
    path('lecture/as_customer/history/',
         CustomerLecturesHistoryGetAPIView.as_view(),
         name='lecture_as_customer_history'),

    path('calendar/lecturer/', LecturerCalendarAPIView.as_view(), name='lecturer_calendar'),
    path('calendar/lecturer/responses/',
         LecturerCalendarResponsesAPIView.as_view(),
         name='lecturer_calendar_responses'),
    path('calendar/customer/', CustomerCalendarAPIView.as_view(), name='customer_calendar'),
    path('calendar/customer/responses/',
         CustomerCalendarResponsesAPIView.as_view(),
         name='customer_calendar_responses'),

    path('lecturer/', LecturerCreateAPIView.as_view(), name='lecturer'),
    path('lecturer/potential_lectures/',
         PotentialLecturerLecturesGetAPIView.as_view(),
         name='potential_lecturer_lectures'),
    path('lecturer/diploma_photos/', DiplomaImageAPIView.as_view(), name='diploma_images'),

    path('customer/', CustomerAPIView.as_view(), name='customer'),
    path('customer/lecturers_list/', LecturersListGetAPIView.as_view(), name='lecturers_list'),
    path('customer/potential_lectures/',
         PotentialCustomerLecturesGetAPIView.as_view(),
         name='potential_customer_lectures'),
]
