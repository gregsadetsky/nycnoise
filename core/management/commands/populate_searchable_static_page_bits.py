from core.models import StaticPage
from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):
        # re-saving every existing static page
        # will run that page's overriden save method
        # which will create the searchable static page bits
        for page in StaticPage.objects.all():
            page.save()
        print("done")
