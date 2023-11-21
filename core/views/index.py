from collections import defaultdict
from datetime import datetime, timedelta

from django.db.models.functions import TruncDate
from django.shortcuts import render
from pytz import timezone

from ..models import DateMessage, Event, Venue


def get_calendar_dates(month=None, today=None):
    """Stealing the calendar date display but mapping events to each day"""

    all_events = (
        Event.objects.all().order_by("starttime").annotate(date=TruncDate("starttime"))
    )
    grouped_events = defaultdict(lambda: 0)
    for event in all_events:
        grouped_events[event.date] += 1
    grouped_events = dict(grouped_events)

    nyctz = timezone("US/Eastern")
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

    date_events = []
    for date in dates_for_calendar:
        events_wording = "events"
        if date in grouped_events:
            num_events = grouped_events[date]
            if num_events == 1:
                events_wording = "event"
        else:
            num_events = 0
            events_wording = "no events"
        date_event_object = {
            "num_events": num_events,
            "events_wording": events_wording,
            "date": date,
            "is_this_month": date.month == month.month,
            "is_today": date == today,
        }
        date_events.append(date_event_object)

    return date_events


def index(request):
    all_events = (
        Event.objects.all().order_by("starttime").annotate(date=TruncDate("starttime"))
    )
    grouped_events = defaultdict(list)
    for event in all_events:
        grouped_events[event.date].append(event)
    all_venues = Venue.objects.all()

    all_messages = DateMessage.objects.all()
    # there might be more than one message per date -- although
    # there shouldn't be? but there might! so store a list
    # ((instead of assuming there will only be a single message,
    # and then overwriting the first message we find for a date
    # with the next message we find for the same date...!))
    date_messages = defaultdict(list)
    for date in all_messages:
        date_messages[date.date].append(date.message)

    return render(
        request,
        "core/index.html",
        {
            # casting to dict since django doesn't deal with defaultdicts well
            # https://stackoverflow.com/a/64666307
            "all_events": dict(grouped_events),
            "all_venues": all_venues,
            "calendar_dates": get_calendar_dates(),
            # as above, don't pass defaultdict's to django templates..!
            "date_messages": dict(date_messages),
        },
    )
