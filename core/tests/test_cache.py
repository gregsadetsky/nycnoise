import uuid

from core.models import Event, Venue
from core.utils_datemath import get_current_new_york_datetime
from django.test import TestCase


class CacheTestCase(TestCase):
    def test_that_changing_event_is_reflected(self):
        title = str(uuid.uuid4())
        description = str(uuid.uuid4())

        venue_name = str(uuid.uuid4())

        venue = Venue.objects.create(name=venue_name)

        event = Event.objects.create(
            title=title,
            description=description,
            venue=venue,
            starttime=get_current_new_york_datetime(),
        )
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, title)

        # change the event title
        new_title = str(uuid.uuid4())
        event.title = new_title
        event.save()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, title)
        self.assertContains(response, new_title)
        self.assertContains(response, venue_name)

        # change the venue name
        new_venue_name = str(uuid.uuid4())
        venue.name = new_venue_name
        venue.save()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, venue_name)
        self.assertContains(response, new_venue_name)
