from django.urls import path

from .views.lector_views import *
from .views.calendar_views import *
from .views.person_views import *


urlpatterns = [
    path('profile/', PersonAPIView.as_view(), name='profile'),
    path('city/', CityAPIView.as_view(), name='city'),

    path('calendar/lecturer/',
         LecturerCalendarCurrentMonthAPIView.as_view(), name='lecturer_calendar'),

    path('lecturer/lecture/', LectorLecturesAPIView.as_view()),
    path('lecturer/lecture/add_to_archive/', ArchiveLecture.as_view()),
]
