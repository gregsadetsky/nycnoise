from collections import defaultdict
from datetime import datetime, timedelta

from dateutil import relativedelta, tz
from django.db.models.functions import TruncDate
from django.shortcuts import render

from ..models import DateMessage, Event, IndexPageMessages, StaticPage
from .search import search
from .static_page import static_page

# DO NOT USE PYTZ <> DO NOT USE PYTZ <> DO NOT USE PYTZ
# https://blog.ganssle.io/articles/2018/03/pytz-fastest-footgun.html
NYCTZ = tz.gettz("America/New_York")


def _get_current_new_york_datetime():
    return datetime.now().astimezone(NYCTZ)


# month_date is any date within the month
# for which the calendar should be generated
def _get_calendar_dates(month_datetime):
    first_day_of_month = month_datetime.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    first_day_on_calendar = first_day_of_month - timedelta(
        days=(first_day_of_month.weekday() + 1) % 7
    )

    dates_for_calendar = [
        first_day_on_calendar + timedelta(days=i) for i in range(0, 42)
    ]

    current_datetime = _get_current_new_york_datetime()

    date_events = []
    for date in dates_for_calendar:
        date_event_object = {
            "date": date,
            "is_current_page_month": date.month == month_datetime.month,
            "is_today": date.date() == current_datetime.date(),
        }
        date_events.append(date_event_object)

    return date_events


# month_datetime can be any (localized!) date time within the month
def _get_events_page_for_month(request, month_datetime, is_index):
    # assert that we're dealing with new york timezone
    assert month_datetime.tzinfo == NYCTZ

    first_day_of_this_month = month_datetime.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    first_day_of_next_month = first_day_of_this_month + relativedelta.relativedelta(
        months=1, day=1
    )

    all_events_for_this_month = (
        Event.objects.filter(
            starttime__gte=first_day_of_this_month,
            starttime__lt=first_day_of_next_month,
        )
        .order_by("starttime", "same_time_order_override")
        .annotate(date=TruncDate("starttime"))
    )

    grouped_events = defaultdict(list)
    for event in all_events_for_this_month:
        grouped_events[event.date].append(event)

    all_messages_for_this_month = DateMessage.objects.filter(
        date__gte=first_day_of_this_month, date__lt=first_day_of_next_month
    )

    # there might be more than one message per date -- store them all as a list
    date_messages = defaultdict(list)
    for date in all_messages_for_this_month:
        date_messages[date.date].append(date.message)

    # use .first() to get either the first object or None.
    # using .get() would raise an exception if the object does not exist in the database
    index_page_messages = IndexPageMessages.objects.first()

    return render(
        request,
        "core/index.html",
        {
            "is_index": is_index,
            "month_year_header": month_datetime.strftime("%Y %B").lower(),
            # casting to dict since django doesn't deal with defaultdicts well
            # https://stackoverflow.com/a/64666307
            "all_events": dict(grouped_events),
            "calendar_dates": _get_calendar_dates(
                month_datetime=first_day_of_this_month
            ),
            # as above, don't pass defaultdict's to django templates..!
            "date_messages": dict(date_messages),
            "index_page_messages": index_page_messages,
        },
    )


def past_month_archive(request, year, month):
    # for past month archive urls i.e. /2023-10/, we FIRST need to check
    # if there was a static page with that content, and return that view instead!
    # otherwise all past months' arvhives wouldn't be available
    archive_url_path = f"{year}-{month}"
    found_archive_page = StaticPage.objects.filter(url_path=archive_url_path).first()
    if found_archive_page:
        # return the static_page view, and pass the full url_path
        # so that the view can render the correct static page
        return static_page(request, url_path=archive_url_path)

    # at this point, assume it's an archive page that we'll be populating ourselves from the db
    month_datetime = datetime(int(year), int(month), 1, 0, 0, 0, 0, tzinfo=NYCTZ)
    return _get_events_page_for_month(
        request, month_datetime=month_datetime, is_index=False
    )


def index(request):
    if request.method == "GET" and request.GET.get("s"):
        # this is actually a search, let the search view handle it!
        return search(request)

    # get current new york first day of month date
    current_datetime = _get_current_new_york_datetime()

    # get the events page based on today
    return _get_events_page_for_month(
        request, month_datetime=current_datetime, is_index=True
    )
