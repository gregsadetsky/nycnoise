from django import template

from ..models import Event
from ..utils import get_gcal_link_from_event as get_gcal_link_from_event_util

register = template.Library()


@register.simple_tag
def get_gcal_link_from_event(event: Event):
    return get_gcal_link_from_event_util(event)
