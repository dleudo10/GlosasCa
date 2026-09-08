from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/glosas/', include('apps.entry.urls'))
]
