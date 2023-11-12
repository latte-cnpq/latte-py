from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/v1/", include("api.urls")),
    path("admin/", admin.site.urls),
]
