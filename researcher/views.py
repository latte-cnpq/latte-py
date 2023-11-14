from .models import Researcher
from .serializers import ResearcherSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.pagination import CustomPagination


class ResearcherViewSet(viewsets.ModelViewSet):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=["get"])
    def search(self, request):
        # Recupera os parâmetros da solicitação
        name = request.query_params.get("name", None)
        email = request.query_params.get("email", None)
        researcher_id = request.query_params.get("researcher_id", None)
        institutes_ids = request.query_params.getlist("institutes", [])

        # Filtra o queryset com base nos parâmetros fornecidos
        queryset = Researcher.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if researcher_id:
            queryset = queryset.filter(researcher_id__icontains=researcher_id)
        if institutes_ids:
            queryset = queryset.filter(institutes__id__in=institutes_ids)

        if not queryset.exists():
            return Response([])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ResearcherSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serializa o resultado e retorna a resposta
        serializer = ResearcherSerializer(queryset, many=True)
        return Response(serializer.data)
