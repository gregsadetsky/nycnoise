import re

import requests
from bs4 import BeautifulSoup
from core.models import StaticPage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # this is a very special handling
        # of [gallery ids="..."] embeds
        # which are a pain to convert when importing them from wordpress.

        # steps, roughly:
        # 1. find all pages with a [gallery ... embed
        all_pages = StaticPage.objects.filter(content__contains="[gallery")
        for page in all_pages:
            # check that there's only one [gallery per page on our site
            if page.content.count("[gallery") > 1:
                raise Exception(f"ERRRR Found more than one [gallery embed on {page}")

            # 2. fetch the current page from nyc-noise.com which has the correct markup
            url_on_existing_site = f"https://nyc-noise.com/{page.url_path}"
            response = requests.get(url_on_existing_site)
            bs = BeautifulSoup(response.text, "html.parser")

            # using beautiful soup, fetch the entire
            # <div data-carousel-extra='...' id='gallery-1' class='gallery ...
            # div

            found_galleries = bs.find_all("div", {"id": re.compile(r"gallery-\d+")})
            assert len(found_galleries) == 1
            found_gallery_str = str(found_galleries[0])

            # 3. do some adjustments:
            # - neuter all links to go to #
            found_gallery_str = re.sub(
                r'<a([^>]+)href="[^"]+"([^>]*)>', r'<a\1href="#"\2>', found_gallery_str
            )

            # edit the <img src=""
            # https://i0.wp.com/nyc-noise.com/wp-content/uploads/2023/03/2023-03-25-sunview.png?resize=150%2C150&amp;ssl=1
            # to point to the s3 bucket
            # make sure to ignore all ?... parts of the url

            found_gallery_str = re.sub(
                r'https://i0.wp.com/nyc-noise.com/wp-content/uploads/([^"?]+)(\?[^"]+|)',
                r"https://nyc-noise-wp-files.s3.us-east-2.amazonaws.com/wp-content/uploads/\1",
                found_gallery_str,
            )

            # replace the [gallery ... embed with the gallery markup
            page.content = re.sub(
                r"\[gallery[^\]]+\]",
                found_gallery_str,
                page.content,
            )

            # save the page
            page.save()
