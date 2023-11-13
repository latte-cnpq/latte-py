from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet,
    PublishedBookViewSet,
    PublishedChapterViewSet,
    ProductionViewSet,
)

router = DefaultRouter()
router.register("", ProductionViewSet, basename="production")
router.register("article", ArticleViewSet, basename="article")
router.register("published-book", PublishedBookViewSet, basename="published-book")
router.register(
    "published-chapter", PublishedChapterViewSet, basename="published-chapter"
)

urlpatterns = [
    path("productions/", include(router.urls)),
]
