from django.db import models
from django.db.models.functions import Upper
from tinymce import models as tinymce_models


class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey("Venue", on_delete=models.SET_NULL, null=True)
    starttime = models.DateTimeField("Start time", null=True)
    description = tinymce_models.HTMLField(max_length=1000, null=True, blank=True)
    hyperlink = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    class Meta:
        # declare default ordering to be case insensitive name ascending
        # case insensitive trick: https://stackoverflow.com/a/52501004
        ordering = [Upper("name")]

    name = models.CharField(max_length=255)
    age_policy = models.CharField(max_length=255, null=True, blank=True)
    neighborhood_and_borough = models.CharField(max_length=255, null=True, blank=True)
    google_maps_link = models.CharField(max_length=255, null=True, blank=True)

    accessibility_emoji = models.CharField(max_length=255, null=True, blank=True)
    accessibility_notes = models.CharField(max_length=255, null=True, blank=True)
    accessibility_link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
