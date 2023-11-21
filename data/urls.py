from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CollaborationGraphViewSet,
    ColumnDataViewSet,
    TotalProductionsViewSet,
    TotalResearchersInstitutesViewSet,
)

router = DefaultRouter()
router.register(
    "collab_graph",
    CollaborationGraphViewSet,
    basename="colaboration_graph",
)
router.register(
    "by-year",
    ColumnDataViewSet,
    basename="by-year",
)
router.register(
    "productions-count", TotalProductionsViewSet, basename="productions-count"
)
router.register("data-count", TotalResearchersInstitutesViewSet, basename="data-count")


urlpatterns = [
    path("data/", include(router.urls)),
]
