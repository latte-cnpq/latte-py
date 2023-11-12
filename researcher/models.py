from django.db import models
from institutes.models import Institute


class Researcher(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField()
    researcher_id = models.CharField(max_length=255)
    resume = models.TextField()
    institutes = models.ManyToManyField(
        Institute, related_name="researchers", blank=True
    )

    def __str__(self):
        return self.name
