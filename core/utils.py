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

    cal_event.add("DTSTART", event.starttime)
    cal_event.add("DTEND", event.starttime + datetime.timedelta(hours=1))
    cal_event.add("CREATED", datetime.datetime.now())
    cal_event.add("UID", uuid.uuid4())
    cal_event.add("SUMMARY", event.title_and_artists)
    cal_event.add("DESCRIPTION", strip_tags(event.description))
    cal_event.add("LOCATION", event.venue_name_and_address)

    cal.add_component(cal_event)
    return cal.to_ical().decode("utf-8")


def get_gcal_link_from_event(event: Event):
    # example link
    # https://www.google.com/calendar/render?action=TEMPLATE&text=Your+Event+Name&dates=20140127T224000Z/20140320T221500Z&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022&sf=true&output=xml

    # it may be ok to assume that the starttime is of utc timezone
    # but it's also kind of never a great idea to assume anything with dates :PPPP
    # convert to isoformat as utc date (i.e. with +0 offset) and the pass off to gcal
    def utcify_and_gcal_isoformat_date(date):
        # https://gist.github.com/danielgross/ca65c8b4e6e7e7483ed1aa8565305a5f#file-quickadd-py-L61
        return date.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    starttime_utc_gcal_iso = utcify_and_gcal_isoformat_date(event.starttime)
    endtime_utc_gcal_iso = utcify_and_gcal_isoformat_date(
        event.starttime + datetime.timedelta(hours=1)
    )

    query_string_params = {
        "action": "TEMPLATE",
        "text": event.title_and_artists,
        "dates": starttime_utc_gcal_iso + "/" + endtime_utc_gcal_iso,
        "details": strip_tags(event.description),
        "sf": "true",
        "output": "xml",
    }

    query_string_params["location"] = event.venue_name_and_address

    query_string = urlencode(query_string_params)
    return "https://www.google.com/calendar/render?" + query_string
