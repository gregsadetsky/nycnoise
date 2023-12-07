import re

from django.conf import settings
from django.db.migrations.recorder import MigrationRecorder
from django.http import HttpResponse, JsonResponse

from ..models import Event, StaticPage, Venue


def internal_db_dump(request):
    """Dump the entire database as JSON.

    This is used by the populate_data_from_prod management command.
    """
    # validate that we were given a developer token
    if not request.headers.get("Authorization"):
        return HttpResponse("Authorization header required", status=401)
    # get bearer token
    res = re.match(r"^Bearer (.+)$", request.headers["Authorization"])
    if not res:
        return HttpResponse("Authorization header malformed", status=401)
    token = res.group(1)
    # validate its len > 0 and validate that it's the same as the settings.conf one we know of
    if not len(token) > 0:
        return HttpResponse("Authorization header required", status=401)
    if token != settings.RC_DEVELOPER_INTERNAL_TOKEN:
        return HttpResponse("Unauthorized", status=401)

    # we should be ok now!

    # return a payload of:
    # the current state of all migrations across all apps to be completely sure
    # that the schema state is identical
    # the events db
    # the venues db

    all_migration_names = MigrationRecorder.Migration.objects.values_list(
        "name", flat=True
    )

    return JsonResponse(
        {
            "all_migration_names": list(all_migration_names),
            "events": list(Event.objects.all().values()),
            "venues": list(Venue.objects.all().values()),
            "static_pages": list(StaticPage.objects.all().values()),
        }
    )
