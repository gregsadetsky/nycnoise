from django.contrib import admin
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE

from .models import DateMessage, Event, Venue

admin.site.site_title = "nyc noise"
admin.site.site_header = "nyc noise"


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "starttime",
        "get_preface_as_text",
        "title",
        "artists",
        "venue",
        "get_description_as_text",
        "price",
        "is_cancelled",
    )
    autocomplete_fields = ("venue",)
    # define a custom order for the fields
    # TODO always keep in sync with the fields in the model..!
    fields = (
        "preface",
        "title",
        "artists",
        "venue",
        "venue_override",
        "starttime",
        "hyperlink",
        "ticket_hyperlink",
        "age_policy_override",
        "description",
        "price",
        "is_cancelled",
    )
    list_display_links = ("starttime",)
    ordering = ("-starttime",)

    class Media:
        js = [
            "core/admin/time-shortcuts-override.js",
        ]
        css = {
            "all": ("core/admin/date-time-widget-fixes.css",),
        }

    # customizing the tinymce field is a painful/weird process.
    # changing the 'rows'/'cols' value (passing them as `attras`), as per the documentation,
    # does nothing... (it changes the <textarea>'s rows and cols attribute values, but that's
    # not taken into account by tinymce, which also receives a width/height value...)
    # TLDR: mce_attrs.height/width is where it's at!!
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ["description", "preface"]:
            return db_field.formfield(
                widget=TinyMCE(
                    mce_attrs={"height": "200"},
                )
            )
        return super().formfield_for_dbfield(db_field, **kwargs)

    def get_preface_as_text(self, obj):
        return mark_safe(obj.preface) if obj.preface else ""

    get_preface_as_text.short_description = "Preface"

    def get_description_as_text(self, obj):
        return mark_safe(obj.description) if obj.description else ""

    get_description_as_text.short_description = "Description"


admin.site.register(Event, EventAdmin)


class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "age_policy", "neighborhood_and_borough")
    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(Venue, VenueAdmin)


class DateMessageAdmin(admin.ModelAdmin):
    list_display = ("date", "message")
    ordering = ("-date",)


admin.site.register(DateMessage, DateMessageAdmin)
