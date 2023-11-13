# views.py

from rest_framework import viewsets
from .models import Production, Article, PublishedBook, PublishedChapter
from .serializers import (
    ProductionSerializer,
    ArticleSerializer,
    PublishedBookSerializer,
    PublishedChapterSerializer,
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class PublishedBookViewSet(viewsets.ModelViewSet):
    queryset = PublishedBook.objects.all()
    serializer_class = PublishedBookSerializer


class PublishedChapterViewSet(viewsets.ModelViewSet):
    queryset = PublishedChapter.objects.all()
    serializer_class = PublishedChapterSerializer


class ProductionViewSet(viewsets.ModelViewSet):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
