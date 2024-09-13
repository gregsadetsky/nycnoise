from django.conf import settings
from django.urls import include, path, re_path

from .views.autocomplete import VenueAutocomplete
from .views.email_subscribe import email_subscribe
from .views.event_gcal import event_gcal_redirect
from .views.event_ics_download import event_ics_download
from .views.event_submission import EventCreateView
from .views.index import index, index_no_cal, past_month_archive
from .views.internal_db_dump import internal_db_dump
from .views.event import event_view

urlpatterns = [
    # main event pages - index and past months
    path("", index),
    path("no_cal", index_no_cal),
    re_path(
        r"^(?P<year>\d{4})-(?P<month>\d{2})/$",
        past_month_archive,
        name="past_month_archive",
    ),
    # other urls
    path("submit-event", EventCreateView.as_view(), name="submit_event"),
    path("event/<int:event_id>/gcal", event_gcal_redirect, name="event_gcal_redirect"),
    path("event/<int:event_id>/ics", event_ics_download, name="event_ics_download"),
    path("event/<int:event_id>", event_view, name="event"),
    path("email-subscribe", email_subscribe, name="email_subscribe"),
    path("internal-api/db", internal_db_dump, name="internal_db_dump"),
    path("venue-autocomplete/", VenueAutocomplete.as_view(), name='venue-autocomplete'),
]

if settings.DEBUG and settings.SHOW_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
