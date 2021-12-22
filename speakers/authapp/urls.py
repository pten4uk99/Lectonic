from django.urls import path
from . import views
from .views import *
urlpatterns = [
  path('registration/', Registration.as_view(), name='registration'),

]