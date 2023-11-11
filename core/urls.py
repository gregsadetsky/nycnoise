from django.urls import path

from .views import event_ics_download, index, internal_db_dump

urlpatterns = [
    path("", index),
    path("event/<int:event_id>/ics", event_ics_download, name="event_ics_download"),
    path("internal-api/db", internal_db_dump, name="internal_db_dump"),
]
