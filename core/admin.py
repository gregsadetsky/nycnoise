import re

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, StaticPage, Venue
from .models import DateMessage, Event, Venue, StaticPage

admin.site.site_title = "nyc noise"
admin.site.site_header = "nyc noise"


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "starttime", "get_description_as_text")
    autocomplete_fields = ("venue",)

    def get_description_as_text(self, obj):
        return mark_safe(obj.description)

    get_description_as_text.short_description = "Description"


admin.site.register(Event, EventAdmin)


class StaticPageAdmin(admin.ModelAdmin):
    list_display = ("url_path", "title", "get_content_as_text")
    search_fields = ("url_path", "title", "content")

    def get_content_as_text(self, obj):
        # extract the first 100 characters, making
        # sure to skip tags
        return re.sub(r"<[^>]*>", "", obj.content)[:100] + "..."

    get_content_as_text.short_description = "Content"


admin.site.register(StaticPage, StaticPageAdmin)


class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "age_policy", "neighborhood_and_borough")
    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(Venue, VenueAdmin)


class DateMessageAdmin(admin.ModelAdmin):
    list_display = ("date", "message")
    ordering = ("-date",)


admin.site.register(DateMessage, DateMessageAdmin)
