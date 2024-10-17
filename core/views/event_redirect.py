from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from core.opengraph import get_meta
from ..models import Event


def event_redirect(request, event_id, tempate_path="core/base.html"):
    event = get_object_or_404(Event, id=event_id)
    if event.starttime or event.starttime_override:
        event_month = (
            event.starttime.strftime("%Y-%m")
            if event.starttime_override is None
            else event.starttime_override.strftime("%Y-%m")
        )
        return render(
            request,
            tempate_path,
            {
                "meta": get_meta(
                    url=request.build_absolute_uri(),
                    redirect=f"/{event_month}/#event-{event_id}",
                )
            },
        )
    else:
        return HttpResponse(status=500)
