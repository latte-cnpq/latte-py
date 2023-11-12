from rest_framework import serializers
from .models import Institute


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = [
            "id",
            "acronym",
            "institute_code",
            "country_acronym",
            "country",
        ]
        read_only_fields = ["id"]
