from collections import defaultdict
from datetime import datetime, timedelta

from django.db.models.functions import TruncDate
from django.http import HttpResponseNotFound
from django.shortcuts import render

from ..models import DateMessage, Event, IndexPageMessages, StaticPage
from ..utils_datemath import (
    NYCTZ,
    beginning_of_day,
    get_current_new_york_datetime,
    get_previous_current_next_month_start,
)
from .search import search
from .static_page import static_page

from ..opengraph import get_meta


# month_date is any date within the month
# for which the calendar should be generated
def _get_calendar_dates(month_datetime, start_today_and_show_3_weeks=False):
    if start_today_and_show_3_weeks:
        first_day_on_calendar = beginning_of_day(get_current_new_york_datetime())

        dates_for_calendar = [
            first_day_on_calendar + timedelta(days=i)
            # 21 days == 3 weeks
            for i in range(0, 3 * 7)
        ]
    else:
        _, first_day_of_month, _ = get_previous_current_next_month_start(month_datetime)

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


# month_datetime can be any (localized!) date time within the month
def _get_events_page_for_month(
    request,
    month_datetime,
    is_index,
    template_path="core/index.html",
    start_today_and_show_3_weeks=False,
):
    # assert that we're dealing with a new york timezone
    assert month_datetime.tzinfo == NYCTZ

    # these are re-used a few times below
    (
        first_day_of_last_month,
        first_day_of_this_month,
        first_day_of_next_month,
    ) = get_previous_current_next_month_start(month_datetime)

    if start_today_and_show_3_weeks:
        events_start_time = beginning_of_day(get_current_new_york_datetime())
        events_end_time = events_start_time + timedelta(weeks=3)
    else:
        events_start_time = first_day_of_this_month
        events_end_time = first_day_of_next_month

    all_events_for_this_month = (
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
    for event in all_events_for_this_month:
        grouped_events[event.date].append(event)

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

    return render(
        request,
        template_path,
        {
            "is_index": is_index,
            "month_year_header": month_datetime.strftime("%Y %B").lower(),
            # casting to dict since django doesn't deal with defaultdicts well
            # https://stackoverflow.com/a/64666307
            "all_events": dict(grouped_events),
            "calendar_dates": _get_calendar_dates(
                month_datetime=events_start_time,
                start_today_and_show_3_weeks=start_today_and_show_3_weeks,
            ),
            # as above, don't pass defaultdict's to django templates..!
            "date_messages": dict(date_messages),
            "index_page_messages": index_page_messages,
            "show_last_curr_next_month_links": start_today_and_show_3_weeks,
            "first_day_of_last_month": first_day_of_last_month,
            "first_day_of_this_month": first_day_of_this_month,
            "first_day_of_next_month": first_day_of_next_month,
            "meta": get_meta()
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


def index_no_cal(request):
    if request.method == "GET" and request.GET.get("s"):
        # this is actually a search, let the search view handle it!
        return search(request)

    # get current new york first day of month date
    current_datetime = get_current_new_york_datetime()

    # get the events page based on today
    return _get_events_page_for_month(
        request,
        month_datetime=current_datetime,
        is_index=True,
        template_path="core/index_no_cal.html",
        start_today_and_show_3_weeks=True,
    )
