from django.urls import path

from adminapp.adminapp_views import *


urlpatterns = [
    path('', signin, name='admin_auth'),
    path('<int:code>', index, name='admin_index'),
    path('make_dump/', make_dump, name='admin_make_dump'),
    path('save_file/', save_file, name='admin_save_file'),
]
