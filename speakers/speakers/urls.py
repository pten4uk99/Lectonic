from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('authapp.urls')),
    path('workroomsapp/', include('workroomsapp.urls')),
]
