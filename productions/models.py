from django.db import models
from researcher.models import Researcher


class Production(models.Model):
    ARTICLE = 1
    BOOK = 2
    CHAPTER = 3
    TYPE_CHOICES = [
        (ARTICLE, "Article"),
        (BOOK, "Published Book"),
        (CHAPTER, "Published Chapter"),
    ]

    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Researcher, related_name="authors")
    title = models.CharField(max_length=255, null=False, blank=False)
    nature = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    language = models.CharField(max_length=50)
    dissemination_medium = models.CharField(max_length=50)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return self.title


class Article(models.Model):
    production = models.OneToOneField(
        Production, on_delete=models.CASCADE, primary_key=True
    )
    periodical_title = models.CharField(max_length=255)
    volume = models.CharField(max_length=255, null=True, blank=True)
    pages = models.CharField(max_length=255, null=True, blank=True)
    publication_location = models.CharField(max_length=255)
    homepage = models.URLField(null=True, blank=True)


class PublishedBook(models.Model):
    production = models.OneToOneField(
        Production, on_delete=models.CASCADE, primary_key=True
    )
    volume = models.CharField(max_length=255, null=True, blank=True)
    pages = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255)


class PublishedChapter(models.Model):
    production = models.OneToOneField(
        Production, on_delete=models.CASCADE, primary_key=True
    )
    book_title = models.CharField(max_length=255, null=True, blank=True)
    organizers = models.TextField()
    pages = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255)
