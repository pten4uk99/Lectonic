from django.urls import path
from .authapp_views import *


urlpatterns = [
    path('signup/', UserCreationView.as_view()),  # POST
    path('login/', UserLoginView.as_view()),  # POST
    path('logout/', UserLogoutView.as_view()),  # GET

    path('delete/', UserDeleteView.as_view()),  # DELETE
]
