# serializers.py

from rest_framework import serializers
from .models import Production, Article, PublishedBook, PublishedChapter


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class PublishedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishedBook
        fields = "__all__"


class PublishedChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishedChapter
        fields = "__all__"


class ProductionSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(source="article_set", many=False, read_only=True)
    published_book = PublishedBookSerializer(
        source="publishedbook", many=False, read_only=True
    )
    published_chapter = PublishedChapterSerializer(
        source="publishedchapter", many=False, read_only=True
    )

    class Meta:
        model = Production
        fields = "__all__"
