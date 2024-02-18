import uuid
from datetime import datetime

from core.models import Event
from dateutil import relativedelta, tz
from django.test import TransactionTestCase


class EventOrderingTestCase(TransactionTestCase):
    serialized_rollback = True

    def test_that_ordered_events_appear_in_order(self):
        nyctz = tz.gettz("America/New_York")
        now_datetime = datetime.now().astimezone(nyctz)

        # same day/hour/minute for the event at 0 seconds
        event_moment = now_datetime.replace(second=0)

        event1_title = f"event {uuid.uuid4()}"
        event1 = Event.objects.create(title=event1_title, starttime=event_moment)

        event2_title = f"event {uuid.uuid4()}"
        event2 = Event.objects.create(title=event2_title, starttime=event_moment)

        # make event1 go before event2
        event1.same_time_order_override = -1
        event1.save()
        event2.same_time_order_override = 1
        event2.save()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event1_title)
        self.assertContains(response, event2_title)

        # check that event1 goes before event 2
        event1_index = response.content.index(event1_title.encode())
        event2_index = response.content.index(event2_title.encode())
        self.assertLess(event1_index, event2_index)

        # change order to event2 before event1
        event1.same_time_order_override = 1
        event1.save()
        event2.same_time_order_override = -1
        event2.save()

        # fetch home page again and check
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event1_title)
        self.assertContains(response, event2_title)

        # check that event2 goes before event 1
        event1_index = response.content.index(event1_title.encode())
        event2_index = response.content.index(event2_title.encode())
        self.assertLess(event2_index, event1_index)

    def test_that_order_does_not_affect_events_at_different_times(self):
        nyctz = tz.gettz("America/New_York")
        now_datetime = datetime.now().astimezone(nyctz)

        # same day/hour/minute for the event at 0 seconds
        event_moment = now_datetime.replace(second=0)

        event1_title = f"event {uuid.uuid4()}"
        event1 = Event.objects.create(title=event1_title, starttime=event_moment)

        event2_title = f"event {uuid.uuid4()}"
        event2 = Event.objects.create(
            title=event2_title,
            starttime=event_moment + relativedelta.relativedelta(minutes=1),
        )

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event1_title)
        self.assertContains(response, event2_title)

        # check that event1 goes before event 2
        event1_index = response.content.index(event1_title.encode())
        event2_index = response.content.index(event2_title.encode())
        self.assertLess(event1_index, event2_index)

        # change ordering -- this should not affect anything
        event1.same_time_order_override = 1000
        event1.save()
        event2.same_time_order_override = -1000
        event2.save()

        # fetch home page again and check
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event1_title)
        self.assertContains(response, event2_title)

        # check that event1 still goes before event2
        event1_index = response.content.index(event1_title.encode())
        event2_index = response.content.index(event2_title.encode())
        self.assertLess(event1_index, event2_index)

        # change order another time in different direction

        event1.same_time_order_override = -1000
        event1.save()
        event2.same_time_order_override = 1000
        event2.save()

        # and check again
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, event1_title)
        self.assertContains(response, event2_title)

        # check that event1 still goes before event2
        event1_index = response.content.index(event1_title.encode())
        event2_index = response.content.index(event2_title.encode())
        self.assertLess(event1_index, event2_index)
