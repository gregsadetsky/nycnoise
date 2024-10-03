from typing import Any
from django.core.management.base import BaseCommand, CommandError
from core.models import Venue
from django.db.models import Q
import time


class Command(BaseCommand):
    help = """
        Reloads coordinates for venues stored in the databse
    """.strip()

    # # customization so that above help string keeps its newlines when printed to the console
    # # https://stackoverflow.com/a/35470682
    # def create_parser(self, *args, **kwargs):
    #     parser = super(Command, self).create_parser(*args, **kwargs)
    #     parser.formatter_class = RawTextHelpFormatter
    #     return parser

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--force",
            default=False,
            help="Force reload venue. In combination with --all reloads all existing venues",
        )
        parser.add_argument(
            "-a",
            "--all",
            default=False,
            help="Load coodnitates for all empty venues in the database. With --force reloads data for everything",
        )
        # parser.add_argument("--delete_all_pages", default=False, action="store_true")
        # parser.add_argument(
        #     "--delete_all_pages_absolutely_for_sure", default=False, action="store_true"
        # )

    def handle(self, *args: Any, **options: Any) -> str | None:
        id = int(4260)  # tv eye
        venues = (
            Venue.objects.all()
            if options["all"] and options["force"]
            else (
                Venue.objects.filter(Q(longitude=None) | Q(latitude=None))
                if options["all"]
                else [Venue.objects.get(pk=id)]
            )
        )

        for v in venues:
            if v.google_maps_link or options["force"]:
                v.reload_coordinates()
                v.save()
            time.sleep(90)
        # return super().handle(*args, **options)
