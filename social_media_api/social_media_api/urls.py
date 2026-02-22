from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('api/accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls')),
    path('api/notifications/', include('notifications.urls')),
]
