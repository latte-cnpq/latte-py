from rest_framework import serializers
from .models import CommonFields, Article, EventWork, PublishedBook, PublishedChapter


class CommonFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonFields
        fields = (
            "id",
            "researcher",
            "title",
            "nature",
            "year",
            "language",
            "dissemination_medium",
        )


# Serializer for Article model
class ArticleSerializer(CommonFieldsSerializer):
    class Meta(CommonFieldsSerializer.Meta):
        model = Article
        fields = CommonFieldsSerializer.Meta.fields + (
            "periodical_title",
            "volume",
            "pages",
            "publication_location",
            "homepage",
        )


# Serializer for EventWork model
class EventWorkSerializer(CommonFieldsSerializer):
    class Meta(CommonFieldsSerializer.Meta):
        model = EventWork
        fields = CommonFieldsSerializer.Meta.fields + (
            "event_name",
            "event_city",
            "pages",
            "publisher_name",
        )


# Serializer for PublishedBook model
class PublishedBookSerializer(CommonFieldsSerializer):
    class Meta(CommonFieldsSerializer.Meta):
        model = PublishedBook
        fields = CommonFieldsSerializer.Meta.fields + ("volume", "pages", "publisher")


# Serializer for PublishedChapter model
class PublishedChapterSerializer(CommonFieldsSerializer):
    class Meta(CommonFieldsSerializer.Meta):
        model = PublishedChapter
        fields = CommonFieldsSerializer.Meta.fields + (
            "book_title",
            "organizers",
            "pages",
            "publisher",
        )
