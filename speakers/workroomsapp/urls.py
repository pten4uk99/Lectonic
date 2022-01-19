from django.urls import path

from .views.person import *

urlpatterns = [
    path('profile/', PersonAPIView.as_view()),
]
