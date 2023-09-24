from django.shortcuts import render

from .models import Event, Venue


def index(request):
    all_events = Event.objects.all()
    all_venues = Venue.objects.all()
    return render(
        request,
        "core/index.html",
        {
            "all_events": all_events,
            "all_venues": all_venues,
        },
    )
