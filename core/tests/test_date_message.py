import uuid
from datetime import datetime

from core.models import DateMessage
from dateutil import tz
from django.test import TestCase


class DateMessageTestCase(TestCase):
    def test_that_date_message_shows_up(self):
        nyctz = tz.gettz("America/New_York")

        now_datetime = datetime.now().astimezone(nyctz)
        message_content = f"message {uuid.uuid4()}"
        DateMessage.objects.create(date=now_datetime, message=message_content)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, message_content)
