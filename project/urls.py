
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include("app.urls")),
    path('example/', include("app_example.urls")),
]
