from django.shortcuts import get_object_or_404, redirect

from ..models import Event
from ..utils import get_gcal_link_from_event


# as noted in templates/index.html, rendering gcal links for all events on the homepage
# was slowing down the template rendering (adding 200ms on prod).
# instead of this, the homepage now includes links to /event/ID/gcal, and only when a link
# is followed does the view below generate the google calendar link and redirects to it
def event_gcal_redirect(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return redirect(get_gcal_link_from_event(event))
