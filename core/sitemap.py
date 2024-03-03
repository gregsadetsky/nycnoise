from django.contrib.sitemaps import Sitemap
from django.db.models.functions import TruncMonth

from .models import Event, StaticPage


class SiteSitemap(Sitemap):
    def items(self):
        url_list = ["/"]

        # all public static pages
        for static_page in StaticPage.objects.all():
            url_list.append(static_page.get_absolute_url())

        # all approved events, extracting the year-month only,
        # and getting a unique list of that
        for event_year_month in set(
            Event.objects.annotate(m=TruncMonth("starttime")).values_list(
                "m", flat=True
            )
        ):
            url_list.append(f"/{event_year_month.year}-{event_year_month.month:02d}/")

        # uniquify.
        return list(set(url_list))

    # locations gets items which are supposed to be objects, and you're supposed
    # to call get_absolute_url on those... but if you already deal with urls, you don't
    # need to do that.
    def location(self, item):
        return item
