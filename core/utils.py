import datetime
import uuid

from django.utils.html import strip_tags
from django.utils.http import urlencode
from icalendar import Calendar
from icalendar import Event as ICalEvent

from .models import Event


def get_ics_string_from_event(event: Event):
    cal = Calendar()
    cal_event = ICalEvent()
    t = event.starttime
    date_start = datetime.datetime(
        t.year, t.month, t.day, t.hour, t.minute, 0, tzinfo=t.tzinfo
    )
    date_end = datetime.datetime(
        t.year, t.month, t.day, (t.hour + 1) % 24, t.minute, tzinfo=t.tzinfo
    )
    cal_event.add("DTSTART", date_start)
    cal_event.add("DTEND", date_end)
    cal_event.add("CREATED", datetime.datetime.now())
    cal_event.add("UID", uuid.uuid4())
    cal_event.add("SUMMARY", event.title_and_artists)
    cal_event.add("DESCRIPTION", strip_tags(event.description))
    cal_event.add("LOCATION", event.venue.name)
    cal.add_component(cal_event)
    return cal.to_ical().decode("utf-8")


def get_gcal_link_from_event(event: Event):
    # example link
    # https://www.google.com/calendar/render?action=TEMPLATE&text=Your+Event+Name&dates=20140127T224000Z/20140320T221500Z&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022&sf=true&output=xml
    start_hour = event.starttime.hour
    end_hour = (event.starttime.hour + 1) % 24
    date_iso_format = event.starttime.date().isoformat().replace("-", "")
    date_start = f"{date_iso_format}T{start_hour}{event.starttime.minute}00Z"
    date_end = f"{date_iso_format}T{end_hour}{event.starttime.minute}00Z"
    query_string_params = {
        "action": "TEMPLATE",
        "text": event.title_and_artists,
        "dates": date_start + "/" + date_end,
        "details": strip_tags(event.description),
        "sf": "true",
        "output": "xml",
    }
    if event.venue.location:
        query_string_params["location"] = event.venue.location
    query_string = urlencode(query_string_params)
    return "https://www.google.com/calendar/render?" + query_string
