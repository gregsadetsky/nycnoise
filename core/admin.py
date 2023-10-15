import re

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, StaticPage, Venue

admin.site.site_title = "nyc noise"
admin.site.site_header = "nyc noise"


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "starttime", "get_description_as_text")

    def get_description_as_text(self, obj):
        return mark_safe(obj.description)

    get_description_as_text.short_description = "Description"


admin.site.register(Event, EventAdmin)

admin.site.register(Venue)


class StaticPageAdmin(admin.ModelAdmin):
    list_display = ("url_path", "title", "get_content_as_text")
    search_fields = ("url_path", "title", "content")

    def get_content_as_text(self, obj):
        # extract the first 100 characters, making
        # sure to skip tags
        return re.sub(r"<[^>]*>", "", obj.content)[:100] + "..."

    get_content_as_text.short_description = "Content"


admin.site.register(StaticPage, StaticPageAdmin)
