from django.urls import path

from .views.calendar_views import *
from .views.lecturer_views import *
from .views.person_views import *


urlpatterns = [
    path('profile/', PersonAPIView.as_view(), name='profile'),
    path('profile/document_photos/', DocumentImageAPIVIew.as_view(), name='document_images'),
    path('city/', CityGetAPIView.as_view(), name='city'),
    path('domain/', DomainGetAPIView.as_view(), name='domain'),

    path('lecturer/', LecturerCreateAPIView.as_view(), name='lecturer'),
    path('lecturer/diploma_photos/', DiplomaImageAPIView.as_view(), name='diploma_images'),
]
