from collections import defaultdict
from datetime import datetime, timedelta

from django.db.models.functions import TruncDate
from django.http import HttpResponseNotFound
from django.shortcuts import render

from ..models import DateMessage, Event, IndexPageMessages, StaticPage
from ..opengraph import get_meta
from ..utils_datemath import (
    NYCTZ,
    beginning_of_day,
    get_current_new_york_datetime,
    get_previous_current_next_month_start,
)
from .search import search
from .static_page import static_page


# _get_calendar_dates can be used for the index page,
# where it is the entire current month (i.e. if now is march 4th, show march)
# OR in case of a month archive (i.e. /2024-03/), it returns that full month
def _get_calendar_dates(month_datetime):
    _, first_day_of_month, _ = get_previous_current_next_month_start(month_datetime)

    # this is math from Rob Simmons to make sure that we always show the entire
    # week that has the first of the month ie if the 1st of the month is a Thursday,
    # we want first_day_on_calendar to be (i.e. start at) the previous Sunday
    # so that the first row of the calendar is "full" ie it starts on the Sunday
    # of the previous month, and then continues for a whole week.
    # NOTE that this means that whenever the first of the month starts on a Sunday,
    # we will not show any dates (on the calendar) from the previous month.
    first_day_on_calendar = first_day_of_month - timedelta(
        days=(first_day_of_month.weekday() + 1) % 7
    )

    dates_for_calendar = [
        first_day_on_calendar + timedelta(days=i)
        # 42 days == 6 weeks
        for i in range(0, 42)
    ]

    current_datetime = get_current_new_york_datetime()

    date_events = []
    for date in dates_for_calendar:
        date_event_object = {
            "date": date,
            "is_current_page_month": date.month == month_datetime.month,
            "is_today": date.date() == current_datetime.date(),
        }
        date_events.append(date_event_object)

    return date_events


def _fetch_events_from_start_to_end_time_group_by_date_as_list(
    events_start_time, events_end_time
):
    fetched_events = (
        # it is very very very important to do a select_related here
        # otherwise this will 100% lead to n+1 sql queries i.e.
        # each time a venue's info is fetched, it will create a new database query.
        # this is truly django's achilles' heel -- not making it obvious that a join
        # is 100% necessary but is 100% not done by default. :-)
        # anyway! select_related!! :-)
        Event.objects.select_related("venue")
        .filter(
            starttime__gte=events_start_time,
            starttime__lt=events_end_time,
        )
        .order_by("starttime", "same_time_order_override")
        .annotate(date=TruncDate("starttime"))
    )

    grouped_events = defaultdict(list)
    for event in fetched_events:
        grouped_events[event.date].append(event)

    grouped_events_as_list = []

    # ITERATE from start to end,
    # and add an object of {"date": date, "events": (list)}
    # to every date
    for day_index in range((events_end_time - events_start_time).days):
        curr_date = (events_start_time + timedelta(days=day_index)).date()
        grouped_events_as_list.append(
            {
                "date": curr_date,
                "events": grouped_events.get(curr_date, []),
            }
        )

    return grouped_events_as_list


def _get_date_and_page_messages_from_start_to_end_time(
    events_start_time, events_end_time
):
    all_messages_for_this_month = DateMessage.objects.filter(
        date__gte=events_start_time, date__lt=events_end_time
    )

    # there might be more than one message per date -- store them all as a list
    date_messages = defaultdict(list)
    for date in all_messages_for_this_month:
        date_messages[date.date].append(date.message)

    # use .first() to get either the first object or None.
    # using .get() would raise an exception if the object does not exist in the database
    index_page_messages = IndexPageMessages.objects.first()

    return (date_messages, index_page_messages)


# month_datetime can be any (localized!) date time within the month
def _get_events_page_for_month(
    request,
    month_datetime,
    is_index,
):
    # assert that we're dealing with a new york timezone
    assert month_datetime.tzinfo == NYCTZ

    # these are used on both index and archive pages
    # to show links at the top and bottom to go to the previews,
    # current and next month.
    # (going to the current month makes sense because the index
    # page now starts at today and shows 3 months, so the current
    # month link allows you to see the full current month.)
    (
        first_day_of_last_month,
        first_day_of_this_month,
        first_day_of_next_month,
    ) = get_previous_current_next_month_start(month_datetime)

    if is_index:
        events_start_time = beginning_of_day(get_current_new_york_datetime())
        events_end_time = events_start_time + timedelta(weeks=3)
    else:
        events_start_time = first_day_of_this_month
        events_end_time = first_day_of_next_month

    grouped_events_as_list = _fetch_events_from_start_to_end_time_group_by_date_as_list(
        events_start_time, events_end_time
    )

    (
        date_messages,
        index_page_messages,
    ) = _get_date_and_page_messages_from_start_to_end_time(
        events_start_time, events_end_time
    )

    return render(
        request,
        "core/index.html",
        {
            "is_index": is_index,
            "month_year_header": month_datetime.strftime("%Y %B").lower(),
            # casting to dict since django doesn't deal with defaultdicts well
            # https://stackoverflow.com/a/64666307
            "grouped_events_as_list": grouped_events_as_list,
            "calendar_dates": _get_calendar_dates(
                month_datetime=events_start_time,
            ),
            # as above, don't pass defaultdict's to django templates..!
            "date_messages": dict(date_messages),
            "index_page_messages": index_page_messages,
            "first_day_of_last_month": first_day_of_last_month,
            "first_day_of_this_month": first_day_of_this_month,
            "first_day_of_next_month": first_day_of_next_month,
            "meta": get_meta(),
        },
    )


def past_month_archive(request, year, month):
    # for past month archive urls i.e. /2023-10/, we FIRST need to check
    # if there was a static page with that content, and return that view instead!
    archive_url_path = f"{year}-{month}"
    found_archive_page = StaticPage.objects.filter(url_path=archive_url_path).first()
    if found_archive_page:
        # return the static_page view, and pass the full url_path
        # so that the view can render the correct static page
        return static_page(request, url_path=archive_url_path)

    valid_date = True
    month_datetime = None

    # at this point, assume it's an archive page that we'll be populating ourselves from the db
    try:
        month_datetime = datetime(int(year), int(month), 1, 0, 0, 0, 0, tzinfo=NYCTZ)
    except ValueError:
        # we were passed a bad month or year e.g. 15 as the value for the month
        valid_date = False

    if valid_date and month_datetime:
        # nycnoise's birth is ~august 2018, any date before that is invalid
        if month_datetime < datetime(2018, 8, 1, 0, 0, 0, 0, tzinfo=NYCTZ):
            valid_date = False
        # anything after 2200? is probably wrong too
        if month_datetime > datetime(2200, 1, 1, 0, 0, 0, 0, tzinfo=NYCTZ):
            valid_date = False

    if not valid_date:
        # if the date is invalid, return a 404
        return HttpResponseNotFound()

    return _get_events_page_for_month(
        request, month_datetime=month_datetime, is_index=False
    )


def index(request):
    if request.method == "GET" and request.GET.get("s"):
        # this is actually a search, let the search view handle it!
        return search(request)

    # get current new york first day of month date
    current_datetime = get_current_new_york_datetime()

    # get the events page based on today
    return _get_events_page_for_month(
        request, month_datetime=current_datetime, is_index=True
    )
