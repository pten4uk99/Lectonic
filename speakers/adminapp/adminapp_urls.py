from django.urls import path

from adminapp.adminapp_views import *


urlpatterns = [
    path('', index, name='admin_index'),
    path('make_dump/', make_dump, name='admin_make_dump'),
    path('save_dump/', save_dump, name='admin_save_dump'),
]
