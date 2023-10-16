from collections import defaultdict

from django.db.models.functions import TruncDay
from django.shortcuts import render

from .models import Event, Venue


def index(request):
    all_events = (
        Event.objects.all().order_by("-starttime").annotate(day=TruncDay("starttime"))
    )
    grouped_events = defaultdict(list)
    grouped_event_gcal_links = list
    for event in all_events:
        grouped_events[event.day].append(event)
        # example link
        # https://www.google.com/calendar/render?action=TEMPLATE&text=Your+Event+Name&dates=20140127T224000Z/20140320T221500Z&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022&sf=true&output=xml
        event_name = event.name.replace(' ', '+')
        print('printing event stuff')
        print(event.starttime.date())
        date_start = f'{event.starttime.date().isoformat().replace("-", "")}T224000Z'
        print(date_start)
        date_end = f'20140320T221500Z'
        details = event.description.replace(' ', '+')
        print(event_name)
        gcal_link = f'https://www.google.com/calendar/render?action=TEMPLATE&text={event_name}'
        grouped_event_gcal_links.append(gcal_link)
        
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
