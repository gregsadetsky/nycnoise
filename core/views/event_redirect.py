from core.opengraph import DEFAULT_TITLE, get_meta
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import date as django_date_format

from ..models import Event
from ..utils_datemath import NYCTZ


def event_redirect(request, event_id, tempate_path="core/empty.html"):
    event = get_object_or_404(Event, id=event_id)
    if not event.starttime:
        return redirect("index")

    event_month = event.starttime.strftime("%Y-%m")

    venue = event.venue_override if event.venue_override else event.venue

    # using django's date filter below
    # (which is typically used in templates as {{ ...|date:"format"}} )
    # because it has the very useful "f" format specifier
    # which is the 12-hour clock with minutes left off if they're zero
    # i.e. '7pm', not '7:00pm'
    event_time = (
        event.starttime_override
        if event.starttime_override
        else django_date_format(event.starttime.astimezone(NYCTZ), "n/j fA").lower()
    )
    event_title = event.title_and_artists if event.title_and_artists else ""
    title = f"{event_time} @ {venue} - {event_title}"

    redirect_time = (
        1 if request.META["HTTP_USER_AGENT"] == "TelegramBot (like TwitterBot)" else 0
    )

    return render(
        request,
        tempate_path,
        {
            "meta": get_meta(
                title=title,
                description=None,
                url=request.build_absolute_uri(),
                redirect=f"/{event_month}/#event-{event_id}",
                redirect_time=redirect_time,
            )
        },
    )
