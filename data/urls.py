from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollaborationGraphViewSet

router = DefaultRouter()
router.register(
    "collab_graph",
    CollaborationGraphViewSet,
    basename="colaboration_graph",
)

urlpatterns = [
    path("data/", include(router.urls)),
]
