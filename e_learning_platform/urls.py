from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('courses.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
]
