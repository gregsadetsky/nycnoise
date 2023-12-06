from django.contrib.sitemaps import Sitemap

from .models import StaticPage


class SiteSitemap(Sitemap):
    def items(self):
        static_pages = StaticPage.objects.all()

        return ["/"] + list(static_pages)

    def location(self, item):
        if isinstance(item, StaticPage):
            return item.get_absolute_url()
        return item
