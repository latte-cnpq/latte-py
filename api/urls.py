from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)


urlpatterns = [
    path("", include("institutes.urls"), name="institutes"),
    path("", include("researcher.urls"), name="researcher"),
    path("", include("productions.urls"), name="productions"),
    path("", include("data.urls"), name="data"),
    path(
        "docs",
        SpectacularRedocView.as_view(),
        name="docs",
    ),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
]
