from django.conf import settings
from django.urls import include, path, re_path

from .views.autocomplete import VenueAutocomplete
from .views.email_subscribe import email_subscribe
from .views.event_gcal import event_gcal_redirect
from .views.event_ics_download import event_ics_download
from .views.event_redirect import event_redirect
from .views.event_submission import EventCreateView
from .views.index import index, past_month_archive
from .views.internal_db_dump import internal_db_dump

urlpatterns = [
    # the two main event page types:
    # - the INDEX ie the homepage ie /
    # which has 1) a "month link toolbar" aka prev/curr/next month links
    # 2) a calendar for the whole current month (i.e. if it's March 14, show March)
    # 3) a list of events which, starting ~March 2025, shows events starting today AND
    # 3 weeks of events into the future
    path("", index),
    # - the monthly archives ie /2025-02/ showing
    # all events for the entire month ie from the first to the last day of the month
    re_path(
        r"^(?P<year>\d{4})-(?P<month>\d{2})/$",
        past_month_archive,
        name="past_month_archive",
    ),
    # other urls
    path("submit-event", EventCreateView.as_view(), name="submit_event"),
    path("event/<int:event_id>/gcal", event_gcal_redirect, name="event_gcal_redirect"),
    path("event/<int:event_id>/ics", event_ics_download, name="event_ics_download"),
    path("email-subscribe", email_subscribe, name="email_subscribe"),
    path("venue-autocomplete/", VenueAutocomplete.as_view(), name="venue-autocomplete"),
    path("event/<int:event_id>", event_redirect, name="event_redirect"),
    # next url is password-protected and lets developers get a copy
    # of the prod data locally
    path("internal-api/db", internal_db_dump, name="internal_db_dump"),
]

if settings.DEBUG and settings.SHOW_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
