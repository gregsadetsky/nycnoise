from collections import defaultdict
from datetime import datetime, timedelta

from django.db.models.functions import TruncDay
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from pytz import timezone

from .models import Event, Venue

from .util import get_ics_string_from_event

nyctz = timezone("US/Eastern")


def calendar_info(month=None, today=None):
    """Create data for a calendar display.

    Creates 7*6 = 42 dates, starting on a Sunday, with the first day
    of the month specified by month somewhere in the first seven
    days.
    """

    current_date = datetime.now(nyctz).date()
    if month is None:
        month = current_date
    if today is None:
        today = current_date

    first_day_of_month = month.replace(day=1)
    first_day_on_calendar = first_day_of_month - timedelta(
        days=(first_day_of_month.weekday() + 1) % 7
    )
    dates_for_calendar = [
        first_day_on_calendar + timedelta(days=i) for i in range(0, 42)
    ]
    return [
        {
            "date": date,
            "is_this_month": date.month == month.month,
            "is_today": date == today,
        }
        for date in dates_for_calendar
    ]


def index(request):
    all_events = (
        Event.objects.all().order_by("-starttime").annotate(day=TruncDay("starttime"))
    )
    grouped_events = defaultdict(list)
    for event in all_events:
        grouped_events[event.day].append(event)
    all_venues = Venue.objects.all()
    return render(
        request,
        "core/index.html",
        {
            # casting to dict since django doesn't deal with defaultdicts well
            # https://stackoverflow.com/a/64666307
            "all_events": dict(grouped_events),
            "all_venues": all_venues,
            "calendar_dates": calendar_info(),
        },
    )


def event_ics_download(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    response = HttpResponse(get_ics_string_from_event(event), content_type="text/calendar")
    response["Content-Disposition"] = "inline; filename=event.ics"
    return response
