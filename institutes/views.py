from .models import Institute
from .serializers import InstituteSerializer
from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response


class InstitutesViewSet(viewsets.ModelViewSet):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
