from django.db import models
from django.utils.http import urlencode
from django.utils.html import strip_tags

from django.db.models.functions import Upper
from tinymce import models as tinymce_models


class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey("Venue", on_delete=models.SET_NULL, null=True)
    starttime = models.DateTimeField("Start time", null=True)
    description = tinymce_models.HTMLField(max_length=1000, null=True, blank=True)
    hyperlink = models.CharField(max_length=255, null=True, blank=True)

    def gcal_link(self):
        # example link
        # https://www.google.com/calendar/render?action=TEMPLATE&text=Your+Event+Name&dates=20140127T224000Z/20140320T221500Z&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022&sf=true&output=xml
        start_hour = self.starttime.hour
        end_hour = (self.starttime.hour + 1) % 24
        date_start = f'{self.starttime.date().isoformat().replace("-", "")}T{start_hour}{self.starttime.minute}00Z'
        date_end = f'{self.starttime.date().isoformat().replace("-", "")}T{end_hour}{self.starttime.minute}00Z'
        query_string = urlencode({
            'action': 'TEMPLATE',
            'text': self.name,
            'dates': date_start + '/' + date_end,
            'details': strip_tags(self.description),
            'location': self.venue.location,
            'sf': 'true',
            'output': 'xml',
        })
        return 'https://www.google.com/calendar/render?' + query_string


    def __str__(self):
        return self.name


class Venue(models.Model):
    class Meta:
        # declare default ordering to be case insensitive name ascending
        # case insensitive trick: https://stackoverflow.com/a/52501004
        ordering = [Upper("name")]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    age_policy = models.CharField(max_length=255, null=True, blank=True)
    neighborhood_and_borough = models.CharField(max_length=255, null=True, blank=True)
    google_maps_link = models.CharField(max_length=255, null=True, blank=True)
    accessibility_emoji = models.CharField(max_length=255, null=True, blank=True)
    accessibility_notes = models.CharField(max_length=255, null=True, blank=True)
    accessibility_link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
