from django.db import models
from researcher.models import Researcher


class CommonFields(models.Model):
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    nature = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    language = models.CharField(max_length=50)
    dissemination_medium = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Article(CommonFields):
    periodical_title = models.CharField(max_length=255)
    volume = models.CharField(max_length=255, null=True, blank=True)
    pages = models.CharField(max_length=255, null=True, blank=True)
    publication_location = models.CharField(max_length=255)
    homepage = models.URLField(null=True, blank=True)


class EventWork(CommonFields):
    event_name = models.CharField(max_length=255)
    event_city = models.CharField(max_length=255)
    pages = models.CharField(max_length=255, null=True, blank=True)
    publisher_name = models.CharField(max_length=255)


class PublishedBook(CommonFields):
    volume = models.CharField(max_length=255, null=True, blank=True)
    pages = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255)


class PublishedChapter(CommonFields):
    book_title = models.CharField(max_length=255, null=True, blank=True)
    organizers = models.TextField()
    pages = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255)
