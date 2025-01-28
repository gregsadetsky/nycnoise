from core.models import Event
from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):
        for event in tqdm(Event.objects.all()):
            event.save()
        print("done")
