from django import template

from django.utils.http import urlencode
from django.utils.html import strip_tags

from ..models import Event

register = template.Library()

@register.simple_tag
def get_gcal_link_from_event(event: Event):
    # example link
    # https://www.google.com/calendar/render?action=TEMPLATE&text=Your+Event+Name&dates=20140127T224000Z/20140320T221500Z&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022&sf=true&output=xml
    start_hour = event.starttime.hour
    end_hour = (event.starttime.hour + 1) % 24
    date_start = f'{event.starttime.date().isoformat().replace("-", "")}T{start_hour}{event.starttime.minute}00Z'
    date_end = f'{event.starttime.date().isoformat().replace("-", "")}T{end_hour}{event.starttime.minute}00Z'
    query_string = urlencode({
        'action': 'TEMPLATE',
        'text': event.name,
        'dates': date_start + '/' + date_end,
        'details': strip_tags(event.description),
        'location': event.venue.location,
        'sf': 'true',
        'output': 'xml',
    })
    return 'https://www.google.com/calendar/render?' + query_string
