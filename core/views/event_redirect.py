from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from core.opengraph import get_meta, DEFAULT_TITLE
from ..models import Event


def event_redirect(request, event_id, tempate_path="core/empty.html"):
    event = get_object_or_404(Event, id=event_id)
    if event.starttime:
        event_month = event.starttime.strftime("%Y-%m")

        venue = event.venue_override if event.venue_override else event.venue
        event_time = (
            event.starttime_override
            if event.starttime_override
            else event.starttime.strftime("%m/%d/%y %H:%M")
        )
        description = f"{event_time} @ {venue}"

        return render(
            request,
            tempate_path,
            {
                "meta": get_meta(
                    title=(
                        event.title_and_artists
                        if event.title_and_artists
                        else DEFAULT_TITLE
                    ),
                    description=description,
                    url=request.build_absolute_uri(),
                    redirect=f"/{event_month}/#event-{event_id}",
                    redirect_time=120,
                )
            },
        )
    else:
        return HttpResponse(status=500)
