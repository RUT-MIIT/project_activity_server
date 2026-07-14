from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/showcase/", include("showcase.urls")),
    path("api/teams/", include("teams.urls")),
    # OpenAPI 3 (drf-spectacular) — источник для Swagger и импорта в Postman
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Алиасы старых URL (ранее drf-yasg)
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="schema-redoc",
    ),
]

# Добавляем маршруты для media файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
