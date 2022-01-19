from django.urls import path

from workroomsapp.views.lector_views import *

urlpatterns = [
    path('lecturer/lecture/add/', AddLecture.as_view()),
    path('lecturer/lecture/delete/', DeleteLecture.as_view()),
    path('lecturer/lecture/modify/', ModifyLecture.as_view()),
    path('lecturer/lecture/show/', GetLecture.as_view()),
    path('lecturer/lectures-list/', GetLectorLectures.as_view()),
]
