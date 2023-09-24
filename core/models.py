from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey("Venue", on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
