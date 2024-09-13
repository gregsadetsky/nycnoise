from django.shortcuts import get_object_or_404, render
from ..models import Event

def event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'core/event_page.html', {"event": event})