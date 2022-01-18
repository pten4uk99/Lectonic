from django.urls import path

from .views.person import *

urlpatterns = [
    path('profile/create/', PersonCreateAPIView.as_view()),
]
