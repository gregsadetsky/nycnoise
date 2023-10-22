from django.db import models
from django.utils.http import urlencode
from django.utils.html import strip_tags

from tinymce import models as tinymce_models


class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey("Venue", on_delete=models.PROTECT)
    starttime = models.DateTimeField("Start time", null=True)
    description = tinymce_models.HTMLField(max_length=1000, null=True, blank=True)

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
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
