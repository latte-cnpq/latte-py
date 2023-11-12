from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitutesViewSet

router = DefaultRouter()
router.register("institutes", InstitutesViewSet, basename="institutes")


urlpatterns = [
    path("", include(router.urls)),
]
