from rest_framework import serializers
from .models import Researcher


class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = ["id", "name", "email", "researcher_id", "resume", "institutes"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        institutes_data = validated_data.pop("institutes", None)
        researcher = Researcher.objects.create(**validated_data)

        if institutes_data:
            researcher.institutes.set(institutes_data)

        return researcher

    def update(self, instance, validated_data):
        institutes_data = validated_data.pop("institutes", None)
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.researcher_id = validated_data.get(
            "researcher_id", instance.researcher_id
        )
        instance.resume = validated_data.get("resume", instance.resume)

        if institutes_data is not None:
            instance.institutes.set(institutes_data)

        instance.save()
        return instance
