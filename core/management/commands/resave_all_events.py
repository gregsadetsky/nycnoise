from core.models import Event
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for event in Event.objects.all():
            event.save()
        print("done")
