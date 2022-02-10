from django.urls import path
from .emailapp_views import *

urlpatterns = [
    path('email_confirmation/', EmailConfirmationView.as_view()),
]
