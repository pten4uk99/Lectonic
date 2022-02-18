from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include

from .utils.yasg import urlpatterns as swagger_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/email/', include('emailapp.emailapp_urls')),
    path('api/auth/', include('authapp.authapp_urls')),
    path('api/workrooms/', include('workroomsapp.workroomsapp_urls')),
    path('api/guest/', include('guestapp.guestapp_urls')),
]

if settings.DEBUG:
    urlpatterns += swagger_urls
