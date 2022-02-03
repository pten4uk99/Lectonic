from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from .utils.yasg import urlpatterns as swagger_urls
from .views import index

urlpatterns = [
    path('', index),
    path('verify_email/', index),
    path('continue_registration/', index),
    path('user_info-form/', index),
    path('user_profile/', index),

    path('admin/', admin.site.urls),

    path('api/email/', include('emailapp.urls')),
    path('api/auth/', include('authapp.urls')),
    path('api/workrooms/', include('workroomsapp.urls')),
    path('api/guest/', include('guestapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += swagger_urls
