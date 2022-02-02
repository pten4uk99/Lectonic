from django.urls import path

from .views import LecturesAPIView, LecturersAPIView

urlpatterns = [
    path('lecture/', LecturesAPIView.as_view()),
    path('lecturer/', LecturersAPIView.as_view()),
]