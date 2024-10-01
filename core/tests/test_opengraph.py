from django.test import TestCase
from core.tests.test_utils import create_static_test_page

expected_domain = "nyc-noise.com"
expected_url = f"https://{expected_domain}/"


class OpengraphTagsTestCase(TestCase):
    def test_opengraph_tags_index(self):
        expected_description = (
            "NYC experimental live music calendar • noise, improv, jazz, new music,"
            " avant-electronics, weirdos • performance against corporate interests!"
        )
        expected_title = "nyc noise"
        expected_image = (
            f"{expected_url}static/core/images/NYC-Noise-facebook-preview-TOO-BIG.png"
        )

        response = self.client.get("/")
        self.assertContains(response, "<title>nyc noise</title>")
        self.assertContains(
            response, f'<meta name="description" content="{expected_description}">'
        )
        self.assertContains(
            response, f'<meta property="og:url" content="{expected_url}">'
        )
        self.assertContains(response, '<meta property="og:type" content="website">')
        self.assertContains(
            response, f'<meta property="og:title" content="{expected_title}">'
        )
        self.assertContains(
            response,
            f'<meta property="og:description" content="{expected_description}">',
        )
        self.assertContains(
            response, f'<meta property="og:image" content="{expected_image}">'
        )
        self.assertContains(
            response, '<meta name="twitter:card" content="summary_large_image">'
        )
        self.assertContains(
            response, f'<meta name="twitter:domain" content="{expected_domain}">'
        )
        self.assertContains(
            response, f'<meta name="twitter:url" content="{expected_url}">'
        )
        self.assertContains(
            response, f'<meta name="twitter:title" content="{expected_title}">'
        )
        self.assertContains(
            response,
            f'<meta name="twitter:description" content="{expected_description}">',
        )
        self.assertContains(
            response, f'<meta name="twitter:image" content="{expected_image}">'
        )

    def test_opengraph_static_page(self):
        page = create_static_test_page()
        response = self.client.get(f"/{page.url_path}/")

        expected_static_url = f"{expected_url}{page.url_path}/"

        self.assertContains(response, f"<title>{page.title}</title>")
        self.assertContains(
            response, f'<meta property="og:url" content="{expected_static_url}">'
        )
        self.assertContains(
            response, f'<meta name="twitter:url" content="{expected_static_url}">'
        )
