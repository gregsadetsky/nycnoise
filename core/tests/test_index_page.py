from django.test import TransactionTestCase


class IndexPageTestCase(TransactionTestCase):
    serialized_rollback = True

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, "nyc noise")
        self.assertContains(response, "always incomplete")
