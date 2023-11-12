from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResearcherViewSet

router = DefaultRouter()
router.register("researcher", ResearcherViewSet, basename="researcher")


urlpatterns = [
    path("", include(router.urls)),
]
