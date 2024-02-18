import uuid
from datetime import datetime

from core.models import Event
from dateutil import tz
from django.test import TestCase


class EventOrderingTestCase(TestCase):
    def test_that_event_at_hour_is_printed_without_minutes(self):
        nyctz = tz.gettz("America/New_York")

        now_datetime = datetime.now().astimezone(nyctz)
        # set hour to 7pm, minute and seconds to 0
        event_moment = now_datetime.replace(hour=19, minute=0, second=0)

        event_title = f"event {uuid.uuid4()}"
        Event.objects.create(title=event_title, starttime=event_moment)

        # getting the homepage i.e. the current/now month
        response = self.client.get("/")

        with open("/tmp/response.html", "wb") as f:
            f.write(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event_title)
        self.assertContains(response, "7pm:")

    def test_that_event_at_half_hour_is_printed_with_minutes(self):
        nyctz = tz.gettz("America/New_York")

        now_datetime = datetime.now().astimezone(nyctz)
        # set hour to 7pm, minute to 30 and seconds to 0
        event_moment = now_datetime.replace(hour=19, minute=30, second=0)

        event_title = f"event {uuid.uuid4()}"
        Event.objects.create(title=event_title, starttime=event_moment)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event_title)
        self.assertContains(response, "7:30pm:")
