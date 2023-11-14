from .models import Institute
from .serializers import InstituteSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.pagination import CustomPagination


class InstitutesViewSet(viewsets.ModelViewSet):
    queryset = Institute.objects.all().order_by("id")
    serializer_class = InstituteSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=["get"])
    def search(self, request):
        # Recupera os parâmetros da solicitação
        acronym = request.query_params.get("acronym", None)
        country = request.query_params.get("country", None)

        # Filtra o queryset com base nos parâmetros fornecidos
        queryset = Institute.objects.all()
        if acronym:
            queryset = queryset.filter(acronym__icontains=acronym)
        if country:
            queryset = queryset.filter(country__icontains=country)

        if not queryset.exists():
            return Response({"results": []})

        # Paginação
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = InstituteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serializa o resultado e retorna a resposta
        serializer = InstituteSerializer(queryset, many=True)
        return Response(serializer.data)
