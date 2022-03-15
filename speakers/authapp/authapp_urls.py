from django.urls import path
from .authapp_views import *


urlpatterns = [
    path('check_authentication/', CheckAuthenticationAPIView.as_view(), name='check_auth'),  # GET
    path('signup/', UserCreationView.as_view(), name='signup'),  # POST
    path('login/', UserLoginView.as_view(), name='login'),  # POST
    path('logout/', UserLogoutView.as_view(), name='logout'),  # GET

    path('delete/', UserDeleteView.as_view()),  # DELETE
]
