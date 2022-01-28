from django.urls import path

from .views import LecturesAPIView

urlpatterns = [
    path('lecture/', LecturesAPIView.as_view()),
]