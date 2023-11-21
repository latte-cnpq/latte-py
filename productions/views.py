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
from django.core.exceptions import ValidationError
from utils.pagination import CustomPagination


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
    pagination_class = CustomPagination

    @action(detail=False, methods=["get"])
    def search(self, request):
        # Recupera os parâmetros da solicitação
        title = request.query_params.get("title", None)
        researcher = request.query_params.get("researcher", None)
        start_year = request.query_params.get("start_year", None)
        end_year = request.query_params.get("end_year", None)
        institute = request.query_params.get("institute", None)
        type = request.query_params.get("type", None)
        language = request.query_params.get("language", None)
        dissemination_medium = request.query_params.get("dissemination_medium", None)

        # Filtra o queryset com base nos parâmetros fornecidos
        queryset = Production.objects.all()
        if title:
            queryset = queryset.filter(title__icontains=title)
        if researcher:
            queryset = queryset.filter(researcher__name__icontains=researcher)
        queryset = queryset.filter(researcher__institutes__acronym__icontains=institute)
        if start_year and end_year:
            try:
                start_year = int(start_year)
                end_year = int(end_year)
                queryset = queryset.filter(year__range=(start_year, end_year))
            except ValueError:
                raise ValidationError("Invalid start_year or end_year format.")
        elif start_year:
            try:
                start_year = int(start_year)
                queryset = queryset.filter(year__gte=start_year)
            except ValueError:
                raise ValidationError("Invalid start_year format.")
        elif end_year:
            try:
                end_year = int(end_year)
                queryset = queryset.filter(year__lte=end_year)
            except ValueError:
                raise ValidationError("Invalid end_year format.")
        if type:
            queryset = queryset.filter(type=type)
        if language:
            queryset = queryset.filter(language__icontains=language)
        if dissemination_medium:
            queryset = queryset.filter(
                dissemination_medium__icontains=dissemination_medium
            )

        print(queryset)

        if not queryset.exists():
            return Response({"results": []})

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serializa o resultado e retorna a resposta
        serializer = ProductionSerializer(queryset, many=True)
        return Response(serializer.data)
