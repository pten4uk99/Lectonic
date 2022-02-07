from django.urls import path

from workroomsapp.views.lector_views import *
from .views.person_views import *

urlpatterns = [
    path('profile/', PersonAPIView.as_view()),
    path('lecturer/lecture/', LectorLecturesAPIView.as_view()),
    path('lecturer/lecture/add_to_archive/', ArchiveLecture.as_view()),
]