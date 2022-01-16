from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', UserProfileCreationView.as_view()),  # POST
    path('login/', UserProfileLoginView.as_view()),  # POST
    path('logout/', UserProfileLogoutView.as_view()),  # POST

    path('lecturer/addlecture/', AddLecture.as_view()),

    path('test/', TestView.as_view()),  # POST
    path('delete/', UserProfileDeleteView.as_view()),  # POST
]
