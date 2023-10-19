from collections import defaultdict

from django.db.models.functions import TruncDay
from django.shortcuts import render

from .models import Event, Venue


def index(request):
    all_events = (
        Event.objects.all().order_by("-starttime").annotate(day=TruncDay("starttime"))
    )
    grouped_events = defaultdict(list)
    event_gcal_links = defaultdict(str)
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
            "gcal_links": dict(event_gcal_links),
        },
    )
