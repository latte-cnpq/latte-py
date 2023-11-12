from .models import Researcher
from .serializers import ResearcherSerializer
from rest_framework import viewsets


class ResearcherViewSet(viewsets.ModelViewSet):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer
