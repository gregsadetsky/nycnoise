import datetime, uuid

from django.utils.html import strip_tags

from icalendar import Event as ICalEvent, Calendar

from .models import Event


def get_ics_string_from_event(event: Event):
    cal = Calendar()
    cal_event = ICalEvent()
    t = event.starttime
    date_start = datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, 0, tzinfo=t.tzinfo)
    date_end = datetime.datetime(t.year, t.month, t.day, (t.hour + 1) % 24, t.minute, tzinfo=t.tzinfo)
    cal_event.add('DTSTART', date_start)
    cal_event.add('DTEND', date_end)
    cal_event.add('CREATED', datetime.datetime.now())
    cal_event.add('UID', uuid.uuid4())
    cal_event.add('SUMMARY', event.name)
    cal_event.add('DESCRIPTION', strip_tags(event.description))
    cal_event.add('LOCATION', event.venue.name)
    cal.add_component(cal_event)
    return cal.to_ical().decode("utf-8")
