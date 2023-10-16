from uuid import uuid4
import datetime
from .models import Event as ModelEvent
from icalendar import Event as ICalEvent, Calendar

def getICSDownloadLinkFromEvent(event: ModelEvent):
    cal = Calendar()
    cal_event = ICalEvent()
    t = event.starttime
    date_start = datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, 0, tzinfo=t.tzinfo)
    date_end = datetime.datetime(t.year, t.month, t.day, (t.hour + 1) % 24, t.minute, tzinfo=t.tzinfo)
    cal_event.add('DTSTART', date_start)
    cal_event.add('DTEND', date_end)
    cal_event.add('CREATED', datetime.datetime.now())
    cal_event.add('UID', uuid4())
    cal_event.add('SUMMARY', event.name)
    cal_event.add('DESCRIPTION', event.description)
    cal_event.add('LOCATION', event.venue.name)
    cal.add_component(cal_event)
    cal.to_ical()
