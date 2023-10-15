from django.db import models
from django.utils import timezone
from tinymce import models as tinymce_models


class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey("Venue", on_delete=models.PROTECT)
    starttime = models.DateTimeField("Start time", null=True)
    description = tinymce_models.HTMLField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StaticPage(models.Model):
    url_path = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField(null=True, blank=True)

    def __str__(self):
        return self.title
