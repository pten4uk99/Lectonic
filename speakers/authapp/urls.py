from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', UserCreationView.as_view()),  # POST
    path('login/', UserLoginView.as_view()),  # POST
    path('logout/', UserLogoutView.as_view()),  # POST


    path('test/', TestView.as_view()),  # POST
    path('delete/', UserDeleteView.as_view()),  # POST
]
