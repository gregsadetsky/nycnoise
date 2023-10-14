from django.shortcuts import render
from django.db.models.functions import TruncDay
from django.db.models import Count
from collections import defaultdict

from .models import Event, Venue


def index(request):
    all_events = Event.objects.all().order_by("-starttime").annotate(day=TruncDay("starttime"))
    grouped_events = defaultdict(list)
    for event in all_events:
        grouped_events[event.day].append(event)
    all_venues = Venue.objects.all()
    return render(
        request,
        "core/index.html",
        {
            "all_events": dict(grouped_events),
            "all_venues": all_venues,
        },
    )
