from django.urls import path

from .views import index, event_ics_download

urlpatterns = [
    path("", index),
    path("event/<int:event_id>/ics", event_ics_download, name="event_ics_download"),
]
