from django.urls import path

from workroomsapp.views.lector_views import *

urlpatterns = [
    path('lecturer/addlecture/', AddLecture.as_view()),
    path('lecturer/lectures-list/', GetLectorLectures.as_view()),
]
