from django.contrib import admin
from django.urls import include, path

from .views import index, event_ics_download, event_month_archive

urlpatterns = [
    path("", index),
    path('event/<int:event_id>/ics', event_ics_download, name="event_ics_download"),
    path("<int:year>-<int:month>", event_month_archive, name="event_month_archive"),
]
