import datetime

from django.db import models
from django.utils.http import urlencode

from tinymce import models as tinymce_models

from icalendar import Event as ICalEvent, Calendar

from uuid import uuid4

from .util import strip_html

class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey("Venue", on_delete=models.PROTECT)
    starttime = models.DateTimeField("Start time", null=True)
    description = tinymce_models.HTMLField(max_length=1000, null=True, blank=True)

    def ics_string(self):
        cal = Calendar()
        cal_event = ICalEvent()
        t = self.starttime
        date_start = datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, 0, tzinfo=t.tzinfo)
        date_end = datetime.datetime(t.year, t.month, t.day, (t.hour + 1) % 24, t.minute, tzinfo=t.tzinfo)
        cal_event.add('DTSTART', date_start)
        cal_event.add('DTEND', date_end)
        cal_event.add('CREATED', datetime.datetime.now())
        cal_event.add('UID', uuid4())
        cal_event.add('SUMMARY', self.name)
        cal_event.add('DESCRIPTION', strip_html(self.description))
        cal_event.add('LOCATION', self.venue.name)
        cal.add_component(cal_event)
        return cal.to_ical().decode("utf-8")

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
            'details': strip_html(self.description),
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
