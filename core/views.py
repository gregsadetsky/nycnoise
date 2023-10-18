from collections import defaultdict

from django.db.models.functions import TruncDay
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Event, Venue

from .util import get_ics_string_from_event


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
        },
    )

def event_ics_download(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    response = HttpResponse(get_ics_string_from_event(event), content_type="text/calendar")
    response['Content-Disposition'] = 'inline; filename=event.ics'
    return response

