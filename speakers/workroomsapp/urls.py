from django.urls import path

from workroomsapp.views.lector import *

urlpatterns = [
    path('lecturer/addlecture/', AddLecture.as_view()),
]
