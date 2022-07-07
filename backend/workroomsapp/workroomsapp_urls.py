from django.urls import path

from workroomsapp.calendar.customer.customer_calendar_views import *
from workroomsapp.calendar.lecturer.lecturer_calendar_views import *
from workroomsapp.lecture.views.as_customer_views import *
from workroomsapp.lecture.views.as_lecturer_views import *
from workroomsapp.lecture.views.lectures_list_views import *
from workroomsapp.lecturer.lecturer_views import *
from workroomsapp.customer.customer_views import *
from workroomsapp.person.person_views import *


urlpatterns = [
    path('profile/', PersonAPIView.as_view(), name='profile'),
    path('city/', CityGetAPIView.as_view(), name='city'),
    path('domain/', DomainGetAPIView.as_view(), name='domain'),

    path('lecture/<int:pk>/', LectureDetailAPIView.as_view(), name='lecture_detail'),
    path('lecture/as_lecturer/', LectureAsLecturerAPIView.as_view(), name='lecture_as_lecturer'),
    path('lecture/as_customer/', LectureAsCustomerAPIView.as_view(), name='lecture_as_customer'),

    # path('lecture/history_list/', LecturesHistoryGetAPIView.as_view(), name='lecture_history'),
    path('lecture/confirmed_list/', ConfirmedLecturesGetAPIView.as_view(), name='lecture_history'),

    path('lecture/response/', LectureResponseAPIView.as_view(), name='lecture_response'),
    path('lecture/cancel_response/', LectureCancelResponseAPIView.as_view(), name='lecture_cancel_response'),
    path('lecture/confirm/', LectureConfirmRespondentAPIView.as_view(), name='lecture_confirm'),
    path('lecture/reject/', LectureRejectRespondentAPIView.as_view(), name='lecture_reject'),

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
    # path('lecturer/diploma_photos/', DiplomaImageAPIView.as_view(), name='diploma_images'),

    path('customer/', CustomerAPIView.as_view(), name='customer'),
    path('customer/lecturers_list/', LecturersListGetAPIView.as_view(), name='lecturers_list'),
    path('customer/potential_lectures/',
         PotentialCustomerLecturesGetAPIView.as_view(),
         name='potential_customer_lectures'),
]
