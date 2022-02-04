from django.urls import path
from .views import *


urlpatterns = [
    path('email_confirmation/', EmailConfirmationView.as_view()),
]