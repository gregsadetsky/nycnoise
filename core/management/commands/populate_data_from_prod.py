from getpass import getpass

import requests
from core.models import Event, Venue
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    def handle(self, *args, **options):
        # ask for rc developer token/password at command line
        developer_token = getpass("Enter your developer token > ")
        # connect to nycnoise.onrender.com/internal-api/db
        # pass token as bearer auth header token
        r = requests.get(
            f"{settings.PROD_INTERNAL_API_SERVER}internal-api/db",
            headers={"Authorization": f"Bearer {developer_token}"},
        )
        # error if wrong password/requests r.ok not ok
        if not r.ok:
            raise CommandError(f"Server returned an error: {r.status_code} {r.reason}")
        server_data = r.json()

        # get state of migrations from server -- compare locally
        # fail if migrations are different -- schema could be different
        local_migration_names = set(
            MigrationRecorder.Migration.objects.values_list("name", flat=True)
        )
        remote_migration_names = set(server_data["all_migration_names"])
        if local_migration_names != remote_migration_names:
            raise CommandError(
                f"Local migrations {local_migration_names} do not match remote migrations {remote_migration_names}"
            )

        # confirm with user that all events and venues will be erased
        # reconfirm a second time
        # reconfirm a third time
        if (
            input(
                "Are you sure you want to ERASE ALL LOCAL EVENTS AND VENUES and replace them with the server's? (yes/no) > "
            )
            != "yes"
        ):
            raise CommandError("not doing anything")

        if (
            input(
                "Are you REALLY REALLY sure you want to ERASE ALL LOCAL EVENTS AND VENUES? (yes/no) > "
            )
            != "yes"
        ):
            raise CommandError("not doing anything")

        if (
            input(
                "Last chance!!!!!!!!!!! Are you REALLY REALLY REALLY sure? (yes/no) > "
            )
            != "yes"
        ):
            raise CommandError("not doing anything")

        print("doing it!!!!")

        # delete all local venues and all local events, import them from server json dump

        Venue.objects.all().delete()
        Event.objects.all().delete()

        Venue.objects.bulk_create(
            Venue(**venue_data) for venue_data in server_data["venues"]
        )
        Event.objects.bulk_create(
            Event(**event_data) for event_data in server_data["events"]
        )
        print("done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
