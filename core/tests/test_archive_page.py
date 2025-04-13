import uuid
from datetime import datetime

from core.models import Event, Venue
from dateutil import relativedelta, tz
from django.test import TestCase
from django.urls import reverse


class ArchivePageTestCase(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(name=f"venue {uuid.uuid4()}")

    def test_event_in_current_month_shows_up_on_index_page(self):
        nyctz = tz.gettz("America/New_York")
        now_datetime = datetime.now().astimezone(nyctz)

        event_title = f"event {uuid.uuid4()}"
        Event.objects.create(
            venue=self.venue,
            title=event_title,
            starttime=now_datetime,
        )

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event_title)

    def test_event_in_current_month_does_not_show_up_on_previous_month_page(self):
        nyctz = tz.gettz("America/New_York")
        now_datetime = datetime.now().astimezone(nyctz)

        event_title = f"event {uuid.uuid4()}"
        Event.objects.create(
            venue=self.venue,
            title=event_title,
            starttime=now_datetime,
        )

        start_of_previous_month = now_datetime.replace(
            day=1
        ) - relativedelta.relativedelta(
            months=1,
        )

        # sanity check -- we should be at least 20 days ahead
        # of last month's 1st day
        assert now_datetime > start_of_previous_month
        assert (now_datetime - start_of_previous_month).days > 20

        archive_page_url = reverse(
            "past_month_archive",
            kwargs={
                "year": start_of_previous_month.year,
                # pad month to 2 digits! urls are 2023-01, not 2023-1
                "month": f"{start_of_previous_month.month:02d}",
            },
        )

        response = self.client.get(archive_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertNotContains(response, event_title)

    def test_event_in_current_month_does_not_show_up_on_next_month_page(self):
        nyctz = tz.gettz("America/New_York")
        now_datetime = datetime.now().astimezone(nyctz)

        event_title = f"event {uuid.uuid4()}"
        Event.objects.create(
            venue=self.venue,
            title=event_title,
            starttime=now_datetime,
        )

        start_of_next_month = now_datetime.replace(day=1) + relativedelta.relativedelta(
            months=1,
        )

        # next month could happen any time - could be tomorrow!
        # so only do sanity check on greater than
        assert start_of_next_month > now_datetime

        archive_page_url = reverse(
            "past_month_archive",
            kwargs={
                "year": start_of_next_month.year,
                # pad month to 2 digits! urls are 2023-01, not 2023-1
                "month": f"{start_of_next_month.month:02d}",
            },
        )

        response = self.client.get(archive_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertNotContains(response, event_title)

    def test_event_in_previous_month_does_not_show_up_on_index_page(self):
        nyctz = tz.gettz("America/New_York")
        now_datetime = datetime.now().astimezone(nyctz)
        start_of_previous_month = now_datetime.replace(
            day=1
        ) - relativedelta.relativedelta(months=1)

        # roughly check that start_of_previous_month is ok
        assert now_datetime > start_of_previous_month
        assert (now_datetime - start_of_previous_month).days > 20

        event_title = f"event {uuid.uuid4()}"
        Event.objects.create(
            venue=self.venue,
            title=event_title,
            starttime=start_of_previous_month,
        )

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertNotContains(response, event_title)
