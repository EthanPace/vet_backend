from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('animals/', include('animals.urls')),
    path('owners/', include('owners.urls')),
    path('visits/', include('visits.urls')),
    path('', include('login.urls')),
]
