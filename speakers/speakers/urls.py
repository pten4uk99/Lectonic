from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from .utils.yasg import urlpatterns as swagger_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/email/', include('emailapp.urls')),
    path('api/auth/', include('authapp.urls')),
    path('api/workrooms/', include('workroomsapp.urls')),
    path('api/guest/', include('guestapp.urls')),
]

if settings.DEBUG:
    urlpatterns += swagger_urls
