from django.urls import path

from .views.email_subscribe import email_subscribe
from .views.event_ics_download import event_ics_download
from .views.index import index
from .views.internal_db_dump import internal_db_dump

urlpatterns = [
    path("", index),
    path("event/<int:event_id>/ics", event_ics_download, name="event_ics_download"),
    path("email-subscribe", email_subscribe, name="email_subscribe"),
    path("internal-api/db", internal_db_dump, name="internal_db_dump"),
]
