from rest_framework import viewsets
from .models import Article, EventWork, PublishedBook, PublishedChapter
from .serializers import (
    ArticleSerializer,
    EventWorkSerializer,
    PublishedBookSerializer,
    PublishedChapterSerializer,
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by("id")
    serializer_class = ArticleSerializer


class EventWorkViewSet(viewsets.ModelViewSet):
    queryset = EventWork.objects.all().order_by("id")
    serializer_class = EventWorkSerializer


class PublishedBookViewSet(viewsets.ModelViewSet):
    queryset = PublishedBook.objects.all().order_by("id")
    serializer_class = PublishedBookSerializer


class PublishedChapterViewSet(viewsets.ModelViewSet):
    queryset = PublishedChapter.objects.all().order_by("id")
    serializer_class = PublishedChapterSerializer
