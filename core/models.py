from django.db import models
from django.db.models.functions import Upper
from icalendar import prop


class Event(models.Model):
    # title and artists are separate fields
    # when both are present, title will be not bold and artists will be bold
    # when either are present, whichever is present will be shown in bold
    title = models.CharField(max_length=255, null=True, blank=True)
    artists = models.CharField(max_length=255, null=True, blank=True)

    venue = models.ForeignKey("Venue", on_delete=models.SET_NULL, null=True, blank=True)
    venue_override = models.CharField(max_length=255, null=True, blank=True)

    starttime = models.DateTimeField("Start time", null=True)
    # `description` will be presented as a tinymce field in the admin
    # because we're overriding `formfield_for_dbfield` in `EventAdmin`.
    # could use HMTLField from tinymce here too, probably, but stick with TextField
    # which we know works.
    description = models.TextField(null=True, blank=True)
    hyperlink = models.CharField(max_length=255, null=True, blank=True)  #
    # some events override the venue's age policy
    age_policy_override = models.CharField(max_length=255, null=True, blank=True)
    # same as `description` - this will be rich text
    preface = models.TextField(null=True, blank=True)

    # optional hyperlink to tickets, separate from event.hyperlink value
    ticket_hyperlink = models.CharField(max_length=255, null=True, blank=True)

    PRICE_RANGE = [
        ("$", "$"),
        ("$$", "$$"),
        ("$$$", "$$$"),
        ("$$$$", "$$$$"),
    ]
    price = models.CharField(max_length=255, choices=PRICE_RANGE, null=True, blank=True)

    # will strikethrough most of the event information, except for the preface
    is_cancelled = models.BooleanField(default=False)

    # make age policy attribute that attempts to fetch its own
    # age policy by default, then tries to get venue's age policy if a venue is set,
    # and otherwise returns none
    @property
    def age_policy(self):
        if self.age_policy_override:
            return self.age_policy_override
        if self.venue:
            return self.venue.age_policy
        # should not happen
        return ""

    @property
    def title_and_artists(self):
        if self.title and self.artists:
            return f"{self.title}: {self.artists}"
        if self.title:
            return self.title
        if self.artists:
            return self.artists
        # should not happen
        return ""

    @property
    def venue_name_and_address(self):
        if self.venue_override:
            return self.venue_override
        if self.venue:
            if self.venue.address:
                return f"{self.venue.name} ({self.venue.address})"
            return self.venue.name
        # should not happen
        return ""

    def __str__(self):
        return self.title_and_artists


class Venue(models.Model):
    class Meta:
        # declare default ordering to be case insensitive name ascending
        # case insensitive trick: https://stackoverflow.com/a/52501004
        ordering = [Upper("name")]

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    age_policy = models.CharField(max_length=255, null=True, blank=True)
    neighborhood_and_borough = models.CharField(max_length=255, null=True, blank=True)
    google_maps_link = models.CharField(max_length=255, null=True, blank=True)
    accessibility_emoji = models.CharField(max_length=255, null=True, blank=True)
    accessibility_notes = models.CharField(max_length=255, null=True, blank=True)
    accessibility_link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class DateMessage(models.Model):
    date = models.DateField("Date", null=True)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.date)
