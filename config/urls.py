from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/showcase/", include("showcase.urls")),
    path("api/teams/", include("teams.urls")),
]

# Добавляем маршруты для media файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
