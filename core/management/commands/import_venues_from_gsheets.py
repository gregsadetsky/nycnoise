import csv

import requests
from core.models import Venue
from django.contrib.postgres.search import TrigramSimilarity
from django.core.management.base import BaseCommand, CommandError

"""
run as:

python manage.py import_venues_from_gsheets SOME-OPTIONS-SEE-BELOW "https://docs.google.com/spreadsheets/d/e/.../pub?output=csv"

to get the /pub?output=csv URL, you must publish the google sheets doc (see the 'File' menu) and choose
csv as the export format. ping greg for the current venue sheets URL.

you MUST pass either --delete_all_venues_and_import_all which will delete everything
and import all venues from google sheets
...OR...
--upsert_venues which will do a similarity search on name and address and attempt
to insert/update only updated venues.

"""

DEBUG_MODE_THAT_DOES_NOT_SAVE = False


def update_venue_object_fields_from_csv_row(venue_obj, csv_row):
    venue_obj.name = csv_row["venue name"]
    venue_obj.name_the = csv_row["the"] == "the"
    venue_obj.address = csv_row["address"]
    venue_obj.age_policy = csv_row["age"]
    venue_obj.neighborhood_and_borough = csv_row["neighborhood+borough"]
    venue_obj.google_maps_link = csv_row["MAP LINK"]

    venue_obj.age_policy_emoji = csv_row["age emoji"]
    venue_obj.accessibility_emoji = csv_row["acc."]
    venue_obj.accessibility_notes = csv_row["access note"]
    venue_obj.accessibility_link = csv_row["access link"]


def get_all_venues_from_google_sheets_csv(url):
    all_venues = []

    r = requests.get(url)
    csv_bytestream = r.content.decode().splitlines()
    csv_reader = csv.DictReader(csv_bytestream)

    for row in csv_reader:
        venue_obj = Venue()
        update_venue_object_fields_from_csv_row(venue_obj, row)
        all_venues.append(venue_obj)

    return all_venues


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("google_sheets_csv_published_url")
        parser.add_argument(
            "--delete_all_venues_and_import_all", default=False, action="store_true"
        )
        parser.add_argument("--upsert_venues", default=False, action="store_true")

    def handle(self, *args, **options):
        if options["upsert_venues"] and options["delete_all_venues_and_import_all"]:
            raise CommandError(
                "You can't use --upsert_venues and --delete_all_venues_and_import_all at the same time"
            )
        if (
            not options["upsert_venues"]
            and not options["delete_all_venues_and_import_all"]
        ):
            raise CommandError(
                "You must use either --upsert_venues or --delete_all_venues_and_import_all"
            )

        # read all venues from google sheets
        all_venues_from_google_sheets = get_all_venues_from_google_sheets_csv(
            options["google_sheets_csv_published_url"]
        )

        if options["delete_all_venues_and_import_all"]:
            user_response = input(
                "About to delete all venues. Are you absolutely sure? Type yes > "
            )
            if user_response != "yes":
                raise CommandError("Aborting")
            Venue.objects.all().delete()

            # import all venues at once and be done with it
            Venue.objects.bulk_create(all_venues_from_google_sheets)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Imported {len(all_venues_from_google_sheets)} venues"
                )
            )
            return

        # at this point, we are doing the upsert process
        assert options["upsert_venues"]

        def update_existing_venue_with_venue_from_google_sheets(
            existing_venue, venue_from_google_sheets
        ):
            update_venue_object_fields_from_csv_row(
                existing_venue, venue_from_google_sheets
            )
            if not DEBUG_MODE_THAT_DOES_NOT_SAVE:
                existing_venue.save()

        nmb_inserted = 0
        nmb_updated = 0

        for venue in all_venues_from_google_sheets:
            # do a similarity search on name and address and filter results that are >0.6 similar
            found_venues = (
                Venue.objects.annotate(similarity=TrigramSimilarity("name", venue.name))
                .filter(similarity__gt=0.6)
                .order_by("-similarity")
            )

            # the fun begins...!
            if len(found_venues) == 0:
                # no matches, so create a new venue
                if not DEBUG_MODE_THAT_DOES_NOT_SAVE:
                    venue.save()
                nmb_inserted += 1
                continue
            elif len(found_venues) == 1:
                # one match, so update the existing venue
                update_existing_venue_with_venue_from_google_sheets(
                    found_venues[0], venue
                )
                nmb_updated += 1
                continue
            elif len(found_venues) > 1:
                # in the case of more than 1, we've seen that we can actually find a perfect match.
                # attempt to find a perfect match using the name. if not found, THEN throw an error
                perfect_match = Venue.objects.filter(name=venue.name)
                if len(perfect_match) == 1:
                    update_existing_venue_with_venue_from_google_sheets(
                        perfect_match[0], venue
                    )
                    nmb_updated += 1
                    continue
                else:
                    raise CommandError(
                        f"ERROR Did not find perfect match for {venue.name}"
                    )
            raise Exception("should never happen", len(found_venues))

        self.stdout.write(
            self.style.SUCCESS(
                f"Upserted {nmb_updated} venues, inserted {nmb_inserted} venues"
            )
        )
