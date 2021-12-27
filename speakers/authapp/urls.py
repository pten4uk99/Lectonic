from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', UserProfileCreationView.as_view()),  # POST
    path('login/', UserProfileLoginView.as_view()),  # POST
]
