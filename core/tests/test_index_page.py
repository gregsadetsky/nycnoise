from django.test import TestCase


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, "nyc noise")
        self.assertContains(response, "always incomplete")
