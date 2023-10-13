from django.shortcuts import render
from datetime import date, timedelta

from .models import Event, Venue


def calendar_info(month=date.today(), today=date.today()):
    """Create data for a calendar display.

    Creates 7*6 = 42 dates, starting on a Sunday, with the first day
    of the month specified by month somewhere in the first seven
    days.
    """

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
            "is_today": date == date.today(),
        }
        for date in dates_for_calendar
    ]


def index(request):
    all_events = Event.objects.all()
    all_venues = Venue.objects.all()
    return render(
        request,
        "core/index.html",
        {
            "calendar_dates": calendar_info(),
            "all_events": all_events,
            "all_venues": all_venues,
        },
    )
