from django.contrib import admin

from .models import Event, Venue

admin.site.site_title = "nyc noise"
admin.site.site_header = "nyc noise"


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "venue")


admin.site.register(Event, EventAdmin)

admin.site.register(Venue)
