import time
from typing import Any

from core.models import Venue
from core.utils_maps import fetch_coordinates
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q


class Command(BaseCommand):
    help = """
        Reload coordinates for venues stored in the database. 
        Waits for the venue IDs as input.
        To update all venues with missing coordinates run with -a flag
    """

    def add_arguments(self, parser):
        parser.add_argument("venue", type=int, nargs="*", help="ID of venues to update")
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Force reload venue. In combination with --all reloads all existing venues",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Load coordinates for all empty venues in the database. With --force reloads data for everything",
        )
        parser.add_argument(
            "-y", "--yes", action="store_true", help="Answer yes to all prompts"
        )
        parser.add_argument(
            "--sleep",
            help="Time to sleep in seconds in between iterations. Defaults to 90 sec",
            default=90,
            type=int,
        )
        parser.add_argument(
            "--skip-sleep", action="store_true", help="Skip sleep in between iterations"
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        if options["force"] and options["all"] and not options["yes"]:
            if (
                input(
                    "Are you REALLY sure you want to refresh everything for ALL VENUES? (yes/no) > "
                )
                != "yes"
            ):
                raise CommandError("not doing anything")

        venues = (
            Venue.objects.all()
            if options["all"] and options["force"]
            else (
                Venue.objects.filter(Q(longitude=None) | Q(latitude=None))
                if options["all"]
                else Venue.objects.filter(pk__in=options["venue"])
            )
        )

        for v in venues:
            if not v.google_maps_link:
                continue

            print(f"Loading coordinates for {v.name}")
            if v.longitude and v.latitude and not options["force"]:
                if (
                    input(
                        f"There ({v.latitude},{v.longitude}) stored for {v.name}. Want to overwrite? (yes/no) > "
                    )
                    != "yes"
                ):
                    continue
            lat, lng = fetch_coordinates(v.google_maps_link)
            if not lat or not lng:
                print(f"Failed to get coordinates for {v.name}")
                continue

            v.latitude, v.longitude = lat, lng
            print(f"Updated location. New location: ({v.latitude},{v.longitude})")
            v.save()

            print(f"Sleeping {options['sleep']} seconds")
            time.sleep(options["sleep"])
