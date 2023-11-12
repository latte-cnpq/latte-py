from django.db import models


from django.db import models


class Institute(models.Model):
    acronym = models.CharField(max_length=255, null=False, blank=False)
    institute_code = models.CharField(max_length=20, null=True, blank=True)
    country_acronym = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.acronym
