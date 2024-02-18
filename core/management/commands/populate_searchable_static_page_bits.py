from core.models import StaticPage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # re-saving every existing static page
        # will run that page's overriden save method
        # which will create the searchable static page bits.
        # exceptionally run this on all_objects to be completely
        # sure that any previously created search vectors for private static pages
        # will be deleted. (saving a private static page deletes the related search vectors)
        for page in StaticPage.all_objects.all():
            page.save()
        print("done")
