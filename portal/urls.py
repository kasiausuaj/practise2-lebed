from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('', include('app.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
