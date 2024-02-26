import uuid
from datetime import datetime

from django.test import TestCase

from core.models import Event, Venue
from core.views.event_submission import UserSubmittedEventForm


class UserSubmittedEventTestCase(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(name=f"venue {uuid.uuid4()}")

    def test_user_cant_submit_empty_event(TestCase):
        """user must include at least a time and either a title or artist info"""
        form = UserSubmittedEventForm()
        assert not form.is_valid()

        form = UserSubmittedEventForm(dict(starttime=datetime.now()))
        assert not form.is_valid()

    def test_user_must_include_some_details(self):
        """ user must include title or artist data """
        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                           title='brutal prog matinée',
                                           venue=self.venue))
        assert form.is_valid()
        form.save()

        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                           artists='grand ulena',
                                           venue=self.venue))
        assert form.is_valid()
        form.save()

        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                           title='brutal prog matinée',
                                           artists='grand ulena',
                                           venue=self.venue))
        assert form.is_valid()
        form.save()

        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                      venue=self.venue))
        assert not form.is_valid()

    def test_user_must_include_venue(self):
        """user must include venue info in either venue or venue_override
        field"""
        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                           title='brutal prog matinée',
                                           artists='grand ulena',
                                           venue=self.venue))
        assert form.is_valid()
        form.save()

        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                           title='brutal prog matinée',
                                           artists='grand ulena',
                                           venue_override='not sure yet'))
        assert form.is_valid()
        form.save()

        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                           artists='some artists',
                                           title='some show'))
        assert not form.is_valid()

    def test_admin_created_events_are_approved(self):
        """events created directly in the admin backend are approved by
        default"""
        event = Event()
        event.save()
        assert event.user_submitted is False
        assert event.is_approved

    def test_user_submitted_events_are_unapproved(self):
        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                           title='brutal prog matinée',
                                           artists='grand ulena',
                                           venue=self.venue))
        event = form.save()
        assert event.user_submitted is True
        assert event.is_approved is False

        form = UserSubmittedEventForm(dict(starttime=datetime.now(),
                                           title='brutal prog matinée',
                                           artists='grand ulena',
                                           venue=self.venue,
                                           is_approved=True))
        event = form.save()
        assert event.user_submitted is True
        assert event.is_approved is False
