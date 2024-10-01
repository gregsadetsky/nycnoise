from core.models import StaticPage
from django.test import TestCase
from core.tests.test_utils import create_static_test_page


class PublicStaticPageTestCase(TestCase):
    def test_public_static_page(self):
        # create a static page
        page = create_static_test_page()
        # check that it's is_public by default
        self.assertTrue(page.is_public)
        # check that its url works
        response = self.client.get(f"/{page.url_path}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/static_page.html")
        self.assertContains(response, page.title)
        self.assertContains(response, page.content)
        # change the is_public property
        page.is_public = False
        page.save()
        # check that we can't fetch it from the db using .objects.
        assert StaticPage.objects.count() == 0
        # check that we can fetch it from the db using .all_objects.
        assert StaticPage.all_objects.count() == 1
        # check that it's not on the site i.e. we get a 404
        response = self.client.get(f"/{page.url_path}/")
        self.assertEqual(response.status_code, 404)
        # make it is_public again
        page.is_public = True
        page.save()
        # check that it appears on the site again
        response = self.client.get(f"/{page.url_path}/")
        self.assertEqual(response.status_code, 200)
        # check that it's fetched once again using .objects.
        assert StaticPage.objects.count() == 1

    def test_static_page_in_sitemap(self):
        # make static page
        # check that it shows up in sitemap
        # make it private
        # check that it doesn't show up in sitemap
        page = create_static_test_page()
        response = self.client.get("/sitemap.xml")
        self.assertContains(response, page.url_path)
        page.is_public = False
        page.save()
        response = self.client.get("/sitemap.xml")
        self.assertNotContains(response, page.url_path)
        page.is_public = True
        page.save()
        response = self.client.get("/sitemap.xml")
        self.assertContains(response, page.url_path)
        page.delete()
        response = self.client.get("/sitemap.xml")
        self.assertNotContains(response, page.url_path)
