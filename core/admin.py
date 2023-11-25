import re

from django.contrib import admin
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from tinymce.widgets import TinyMCE

from .models import (
    DateMessage,
    EmailSubscriber,
    Event,
    IndexPageMessages,
    StaticPage,
    Venue,
)

admin.site.site_title = "nyc noise"
admin.site.site_header = "nyc noise"


admin.site.register(IndexPageMessages, SingletonModelAdmin)


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
        "starttime",
        "hyperlink",
        "title",
        "artists",
        "venue",
        "ticket_hyperlink",
        "description",
        "preface",
        "starttime_override",
        "venue_override",
        "age_policy_override",
        "price",
        "is_cancelled",
    )
    list_display_links = ("starttime",)
    ordering = ("-starttime",)
    save_on_top = True
    # there are move save_* options that are being overriden
    # in templatetags/admin_save_buttons_override --
    # namely, the fact that both 'save as new' and 'save and add another' buttons
    # appear simultanously is not something that can be set using 'regular'
    # django admin options
    search_fields = (
        "title",
        "artists",
        "venue__name",
        "description",
        "preface",
    )

    # this is insane, I've (greg) been using django for 16+ years,
    # I ***did not know*** this was a thing. this is bonkers.
    list_editable = (
        "is_cancelled",
        "title",
        "artists",
        "venue",
        "price",
    )

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
                    mce_attrs={
                        "height": "200" if db_field.name == "description" else "150"
                    }
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
    list_display = (
        "name_the_string",
        "name",
        "address",
        "age_policy",
        "neighborhood_and_borough",
    )
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    save_on_top = True

    def name_the_string(self, obj):
        return "the" if obj.name_the else ""

    name_the_string.short_description = "The"


admin.site.register(Venue, VenueAdmin)


class DateMessageAdmin(admin.ModelAdmin):
    list_display = ("date", "message")
    ordering = ("-date",)


admin.site.register(DateMessage, DateMessageAdmin)


class EmailSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    ordering = ("-created_at",)


admin.site.register(EmailSubscriber, EmailSubscriberAdmin)
