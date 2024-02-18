import uuid

from core.models import Event, StaticPage
from core.utils_datemath import get_current_new_york_datetime
from django.test import TestCase


class SearchTestCase(TestCase):
    def test_static_page_search(self):
        # create a static page, stuff an uuid in it,
        # then search for it

        page_path = str(uuid.uuid4())
        page_title = str(uuid.uuid4())
        page_content = str(uuid.uuid4())
        static_page = StaticPage.objects.create(
            url_path=page_path, title=page_title, content=page_content, is_public=True
        )
        # check that the page exists and has our content
        response = self.client.get(f"/{page_path}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, page_content)

        partial_content = page_content[-12:]
        # search for content
        response = self.client.get("/", {"s": partial_content})
        self.assertEqual(response.status_code, 200)
        # find the static page's title in the results
        self.assertContains(response, page_title)

        # make page private
        static_page.is_public = False
        static_page.save()
        # search for content
        response = self.client.get("/", {"s": partial_content})
        self.assertEqual(response.status_code, 200)
        # assert that we cannot find static page's title in the results
        self.assertNotContains(response, page_title)

    def test_database_event_search(self):
        # create event
        event_title = str(uuid.uuid4())
        event_description = str(uuid.uuid4())
        Event.objects.create(
            title=event_title,
            description=event_description,
            starttime=get_current_new_york_datetime(),
        )
        partial_title = event_title[-12:]
        # search for event
        response = self.client.get("/", {"s": partial_title})

        self.assertEqual(response.status_code, 200)
        # find the title and the description in the results
        self.assertContains(response, event_title)
        self.assertContains(response, event_description)
