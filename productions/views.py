# views.py

from .models import Production, Article, PublishedBook, PublishedChapter
from .serializers import (
    ProductionSerializer,
    ArticleSerializer,
    PublishedBookSerializer,
    PublishedChapterSerializer,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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

    @action(detail=False, methods=["get"])
    def search(self, request):
        # Recupera os parâmetros da solicitação
        title = request.query_params.get("title", None)
        researcher = request.query_params.get("researcher", None)
        year = request.query_params.get("year", None)
        types = request.query_params.getlist("types", None)
        language = request.query_params.get("language", None)
        dissemination_medium = request.query_params.get("dissemination_medium", None)

        # Filtra o queryset com base nos parâmetros fornecidos
        queryset = Production.objects.all()
        if title:
            queryset = queryset.filter(title__icontains=title)
        if researcher:
            queryset = queryset.filter(researcher__name__icontains=researcher)
        if year:
            queryset = queryset.filter(year=year)
        if types:
            queryset = queryset.filter(type__in=types)
        if language:
            queryset = queryset.filter(language__icontains=language)
        if dissemination_medium:
            queryset = queryset.filter(
                dissemination_medium__icontains=dissemination_medium
            )

        # Paginação
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serializa o resultado e retorna a resposta
        serializer = ProductionSerializer(queryset, many=True)
        return Response(serializer.data)
