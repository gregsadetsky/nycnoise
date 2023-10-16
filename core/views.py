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
        # example link
        # https://www.google.com/calendar/render?action=TEMPLATE&text=Your+Event+Name&dates=20140127T224000Z/20140320T221500Z&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022&sf=true&output=xml
        event_name = event.name.replace(' ', '+')
        print('printing event stuff')
        print(event_name)
        start_hour = event.starttime.hour
        end_hour = (event.starttime.hour + 1) % 24
        date_start = f'{event.starttime.date().isoformat().replace("-", "")}T{start_hour}{event.starttime.minute}00Z'
        date_end = f'{event.starttime.date().isoformat().replace("-", "")}T{end_hour}{event.starttime.minute}00Z'
        gcal_link = f'https://www.google.com/calendar/render?action=TEMPLATE'
        gcal_link += f'&text={event_name}'
        gcal_link += f'&dates={date_start}/{date_end}'
        gcal_link += f'&details={event.description.replace(" ", "+")}'
        gcal_link += f'&location={event.venue.location}'
        gcal_link += '&sf=true&output=xml'
        event_gcal_links[event_name] = gcal_link
    

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
