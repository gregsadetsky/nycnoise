from django.test import Client, TestCase
from django.test.utils import ignore_warnings


class IndexPageTestCase(TestCase):
    def setUp(self):
        ignore_warnings(message="No directory at", module="whitenoise.base").enable()
        self.client = Client()

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, "nyc noise")
        self.assertContains(response, "always incomplete")
