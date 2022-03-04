from django.urls import path

from .views.calendar_views import *
from .views.lecturer_views import *
from .views.person_views import *


urlpatterns = [
    path('profile/', PersonAPIView.as_view(), name='profile'),
    path('profile/upload_document/', DocumentImageCreateAPIVIew.as_view(), name='document_image'),
    path('city/', CityAPIView.as_view(), name='city'),

    path('calendar/lecturer/', LecturerCalendarAPIView.as_view(), name='lecturer_calendar'),

    path('lecturer/', LecturerCreateAPIView.as_view(), name='lecturer'),
]
