from django.urls import path

from workroomsapp.views.lector_views import *
from .views.person import *

urlpatterns = [
    path('profile/', PersonAPIView.as_view()),
    path('lecturer/lecture/', LectorLecturesAPIView.as_view()),
    path('lecturer/lecture/delete-multiple/', DeleteMultipleLecture.as_view()),
]