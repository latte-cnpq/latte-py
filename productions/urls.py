from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet,
    EventWorkViewSet,
    PublishedBookViewSet,
    PublishedChapterViewSet,
)

router = DefaultRouter()
router.register("article", ArticleViewSet, basename="article")
router.register("event-work", EventWorkViewSet, basename="event-work")
router.register("published-book", PublishedBookViewSet, basename="published-book")
router.register(
    "published-chapter", PublishedChapterViewSet, basename="published-chapter"
)

urlpatterns = [
    path("productions/", include(router.urls)),
]
