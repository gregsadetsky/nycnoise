from django import template
from .models import Event

register = template.Library()


@register.simple_tag
def gcal_link(event: Event):
    # example link
    # https://www.google.com/calendar/render?action=TEMPLATE&text=Your+Event+Name&dates=20140127T224000Z/20140320T221500Z&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022&sf=true&output=xml
    start_hour = event.starttime.hour
    end_hour = (event.starttime.hour + 1) % 24
    date_start = f'{event.starttime.date().isoformat().replace("-", "")}T{start_hour}{event.starttime.minute}00Z'
    date_end = f'{event.starttime.date().isoformat().replace("-", "")}T{end_hour}{event.starttime.minute}00Z'
    gcal_link = f'https://www.google.com/calendar/render?action=TEMPLATE'
    gcal_link += f'&text={event.name.replace(" ", "+")}'
    gcal_link += f'&dates={date_start}/{date_end}'
    gcal_link += f'&details={event.description.replace(" ", "+")}'
    gcal_link += f'&location={event.venue.location.replace(" ", "+")}'
    gcal_link += '&sf=true&output=xml'
    return gcal_link
