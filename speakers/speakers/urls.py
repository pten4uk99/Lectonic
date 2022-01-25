from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include

from .utils.yasg import urlpatterns as swagger_urls
from workroomsapp.views.guest_views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('authapp.urls')),
    path('api/workrooms/', include('workroomsapp.urls')),
    path('api/lecture/', LecturesAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += swagger_urls
