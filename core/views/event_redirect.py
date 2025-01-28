from core.opengraph import DEFAULT_TITLE, get_meta
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Event
from ..utils_datemath import NYCTZ


def event_redirect(request, event_id, tempate_path="core/empty.html"):
    event = get_object_or_404(Event, id=event_id)
    if not event.starttime:
        return redirect("index")

    event_month = event.starttime.strftime("%Y-%m")

    venue = event.venue_override if event.venue_override else event.venue
    event_time = (
        event.starttime_override
        if event.starttime_override
        else event.starttime.astimezone(NYCTZ).strftime("%m/%d %-I:%M %p").lower()
    )
    event_title = event.title_and_artists if event.title_and_artists else ""
    title = f"{event_time} @ {venue} - {event_title}"

    redirect_time = (
        1
        if request.META["HTTP_USER_AGENT"] == "TelegramBot (like TwitterBot)"
        else 0
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
