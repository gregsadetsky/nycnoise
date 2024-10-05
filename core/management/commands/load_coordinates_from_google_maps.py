from typing import Any
from django.core.management.base import BaseCommand, CommandError
from core.models import Venue
from django.db.models import Q
import time


class Command(BaseCommand):
    help = """
        Reload coordinates for venues stored in the databse. 
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
            help="Load coodnitates for all empty venues in the database. With --force reloads data for everything",
        )
        parser.add_argument(
            "-y", "--yes", action="store_true", help="Answer yes to all prompts"
        )
        parser.add_argument(
            "--sleep",
            help="Time to sleep in seconds in between interations. Defaults to 90 sec",
            default=90,
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
            if v.google_maps_link or options["force"]:
                print(f"Loading coodrinates for {v.name}")
                if v.longitude and v.latitude and not options["force"]:
                    if (
                        input(
                            f"There ({v.latitude},{v.longitude}) stored for {v.name}. Want to overwrtie? (yes/no) > "
                        )
                        != "yes"
                    ):
                        continue
                if v.reload_coordinates():
                    print(
                        f"Updated location. New location: ({v.latitude},{v.longitude})"
                    )
                else:
                    print("Not updated. A problem")
                v.save()
            if v != venues[len(venues) - 1] and not options["skip_sleep"]:
                print(f"Sleeping {options['sleep']} seconds")
                time.sleep(options["sleep"])
