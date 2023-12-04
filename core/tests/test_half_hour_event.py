import uuid
from datetime import datetime

from core.models import Event
from dateutil import tz
from django.test import TestCase


class EventOrderingTestCase(TestCase):
    def test_that_event_at_hour_is_printed_without_minutes(self):
        nyctz = tz.gettz("America/New_York")
        event_moment = datetime(2023, 12, 3, 19, 0, 0, 0).astimezone(nyctz)

        event_title = f"event {uuid.uuid4()}"
        Event.objects.create(title=event_title, starttime=event_moment)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event_title)
        self.assertContains(response, "7pm:")

    def test_that_event_at_half_hour_is_printed_with_minutes(self):
        nyctz = tz.gettz("America/New_York")
        event_moment = datetime(2023, 12, 3, 19, 30, 0, 0).astimezone(nyctz)

        event_title = f"event {uuid.uuid4()}"
        Event.objects.create(title=event_title, starttime=event_moment)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event_title)
        self.assertContains(response, "7:30pm:")
