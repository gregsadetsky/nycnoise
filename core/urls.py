from django.urls import path, re_path

from .views.email_subscribe import email_subscribe
from .views.event_ics_download import event_ics_download
from .views.index import index, past_month_archive
from .views.internal_db_dump import internal_db_dump

urlpatterns = [
    # main event pages - index and past months
    path("", index),
    re_path(r"^(\d{4})-(\d{2})/$", past_month_archive, name="past_month_archive"),
    # other urls
    path("event/<int:event_id>/ics", event_ics_download, name="event_ics_download"),
    path("email-subscribe", email_subscribe, name="email_subscribe"),
    path("internal-api/db", internal_db_dump, name="internal_db_dump"),
]
