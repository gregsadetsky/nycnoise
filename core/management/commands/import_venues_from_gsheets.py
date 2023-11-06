import csv

import requests
from core.models import Venue
from django.core.management.base import BaseCommand, CommandError

"""
run as:

python manage.py import_venues_from_gsheets "https://docs.google.com/spreadsheets/d/e/.../pub?output=csv"

to get the /pub?output=csv url, you must publish the google sheets doc (see the 'File' menu) and choose
csv as the export format

"""


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("google_sheets_csv_published_url")
        parser.add_argument("--delete_all_venues", default=False, action="store_true")

    def handle(self, *args, **options):
        if options["delete_all_venues"]:
            user_response = input(
                "About to delete all venues. Are you absolutely sure? Type yes > "
            )
            if user_response != "yes":
                raise CommandError("Aborting")
            Venue.objects.all().delete()

        r = requests.get(options["google_sheets_csv_published_url"])
        csv_bytestream = r.content.decode().splitlines()
        csv_reader = csv.DictReader(csv_bytestream)

        imported_venues = 0
        for row in csv_reader:
            venue_obj = Venue()

            venue_obj.name = row["venue name"]
            venue_obj.address = row["address"]
            venue_obj.age_policy = row["age"]
            venue_obj.neighborhood_and_borough = row["neighborhood+borough"]
            venue_obj.google_maps_link = row["MAP LINK"]

            venue_obj.accessibility_emoji = row["acc."]
            venue_obj.accessibility_notes = row["access note"]
            venue_obj.accessibility_link = row["access link"]

            venue_obj.save()
            imported_venues += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {imported_venues} venues"))
