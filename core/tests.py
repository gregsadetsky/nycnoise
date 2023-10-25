from django.test import TestCase
from django.urls import reverse
from .models import Event, Venue
import datetime

class ArchiveTestCase(TestCase):
    def setUp(self):
        venue = Venue.objects.create(
            name="Recurse Center",
            location="397 Bridge St, Brooklyn, NY 11201",
            age_policy="18+",
            neighborhood_and_borough="",
            google_maps_link="https://maps.app.goo.gl/moRm2h2e7vkEmBmz8",
            accessibility_emoji="",
            accessibility_notes="",
            accessibility_link="",
        )
        
        Event.objects.create(
            name="cool event",
            venue=venue,
            starttime ="2023-04-15T12:00:00Z",
        )

    def test_archive_works(self):
        url = reverse('event_month_archive', args=(2023, 4))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["year"], 2023)
        self.assertEqual(response.context["month"], "April")
        self.assertEqual(len(response.context["events"]), 1)
        self.assertEqual(response.context["events"][datetime.date(2023, 4, 15)][0].name, "cool event")
        self.assertEqual(response.context["events"][datetime.date(2023, 4, 15)][0].age_policy, "18+")
