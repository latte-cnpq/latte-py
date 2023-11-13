from .models import Researcher
from .serializers import ResearcherSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ResearcherViewSet(viewsets.ModelViewSet):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer

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

        # Serializa o resultado e retorna a resposta
        serializer = ResearcherSerializer(queryset, many=True)
        return Response(serializer.data)
