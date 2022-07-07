from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from .utils.yasg import urlpatterns as swagger_urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/lectonic_admin/', include('adminapp.adminapp_urls')),

    path('api/email/', include('emailapp.emailapp_urls')),
    path('api/auth/', include('authapp.authapp_urls')),
    path('api/workrooms/', include('workroomsapp.workroomsapp_urls')),
    path('api/chat/', include('chatapp.chatapp_urls')),
]

if settings.DEBUG:
    urlpatterns += swagger_urls
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
