import uuid
from http import HTTPStatus

from core.models import Event, Venue
from core.views.event_submission import UserSubmittedEventForm
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class UserSubmittedEventTestCase(TestCase):
    endpoint = reverse("submit_event")

    def setUp(self):
        self.venue = Venue.objects.create(name=f"venue {uuid.uuid4()}")

    def test_get(self):
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>Submit Event</h1>", html=True)

    def test_post_success(self):
        form = UserSubmittedEventForm(
            dict(
                starttime=timezone.now(),
                title="brutal prog matinée",
                artists="grand ulena",
                venue=self.venue.pk,
            )
        )

        response = self.client.post(
            self.endpoint, data=form.data, follow=True
        )  # follow redirect so we can use assertContains on content

        self.assertContains(response, "event is submitted for approval")

    def test_unapproved_events_are_hidden(self):
        admin_event = Event(title=uuid.uuid4(), starttime=timezone.now())
        admin_event.save()

        unapproved_event = UserSubmittedEventForm(
            dict(starttime=timezone.now(), title=uuid.uuid4(), venue=self.venue.pk)
        ).save()
        response = self.client.get("/")
        self.assertContains(response, admin_event.title)
        self.assertNotContains(response, unapproved_event.title)

    def test_approved_events_are_shown(self):
        admin_event = Event(title=uuid.uuid4(), starttime=timezone.now())
        admin_event.save()

        submitted_event = UserSubmittedEventForm(
            dict(starttime=timezone.now(), title=uuid.uuid4(), venue=self.venue.pk)
        ).save()
        submitted_event.is_approved = True
        submitted_event.save()

        response = self.client.get("/")
        self.assertContains(response, admin_event.title)
        self.assertContains(response, submitted_event.title)

    def test_post_error(self):
        form = UserSubmittedEventForm(
            dict(starttime=timezone.now(), venue=self.venue.pk)
        )

        response = self.client.post(self.endpoint, data=form.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "event must include title or artists")

    def test_user_cant_submit_empty_event(TestCase):
        """user must include at least a time and either a title or artist info"""
        form = UserSubmittedEventForm()
        assert not form.is_valid()

        form = UserSubmittedEventForm(dict(starttime=timezone.now()))
        assert not form.is_valid()

    def test_user_must_include_some_details(self):
        """user must include title or artist data"""
        form = UserSubmittedEventForm(
            dict(
                starttime=timezone.now(), title="brutal prog matinée", venue=self.venue
            )
        )
        assert form.is_valid(), form.errors
        form.save()

        form = UserSubmittedEventForm(
            dict(starttime=timezone.now(), artists="grand ulena", venue=self.venue)
        )
        assert form.is_valid(), form.errors
        form.save()

        form = UserSubmittedEventForm(
            dict(
                starttime=timezone.now(),
                title="brutal prog matinée",
                artists="grand ulena",
                venue=self.venue,
            )
        )
        assert form.is_valid(), form.errors
        form.save()

        form = UserSubmittedEventForm(dict(starttime=timezone.now(), venue=self.venue))
        assert not form.is_valid()

    def test_user_must_include_venue(self):
        """user must include venue info in either venue or venue_override
        field"""
        form = UserSubmittedEventForm(
            dict(
                starttime=timezone.now(),
                title="brutal prog matinée",
                artists="grand ulena",
                venue=self.venue,
            )
        )
        assert form.is_valid(), form.errors
        form.save()

        form = UserSubmittedEventForm(
            dict(
                starttime=timezone.now(),
                title="brutal prog matinée",
                artists="grand ulena",
                venue_override="not sure yet",
            )
        )
        assert form.is_valid(), form.errors
        form.save()

        form = UserSubmittedEventForm(
            dict(starttime=timezone.now(), artists="some artists", title="some show")
        )
        assert not form.is_valid()

    def test_admin_created_events_are_approved(self):
        """events created directly in the admin backend are approved by
        default"""
        event = Event()
        event.save()
        assert event.user_submitted is False
        assert event.is_approved

    def test_user_submitted_events_are_unapproved(self):
        form = UserSubmittedEventForm(
            dict(
                starttime=timezone.now(),
                title="brutal prog matinée",
                artists="grand ulena",
                venue=self.venue,
            )
        )
        event = form.save()
        assert event.user_submitted is True
        assert event.is_approved is False

        form = UserSubmittedEventForm(
            dict(
                starttime=timezone.now(),
                title="brutal prog matinée",
                artists="grand ulena",
                venue=self.venue,
                is_approved=True,
            )
        )
        event = form.save()
        assert event.user_submitted is True
        assert event.is_approved is False

    def test_closed_venues_not_shown_in_list(self):
        open_venue = Venue(name=uuid.uuid4().hex)
        closed_venue = Venue(name=uuid.uuid4().hex, closed=True)
        open_venue.save()
        closed_venue.save()

        response = self.client.get(self.endpoint)
        self.assertContains(response, open_venue.name)
        self.assertNotContains(response, closed_venue.name)
