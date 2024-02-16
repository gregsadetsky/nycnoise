from django.db import models
from django.db.models.functions import Upper
from django.urls import reverse
from ordered_model.models import OrderedModel
from solo.models import SingletonModel
from tinymce import models as tinymce_models


class Event(models.Model):
    # title and artists are separate fields
    # when both are present, title will be not bold and artists will be bold
    # when either are present, whichever is present will be shown in bold
    title = models.CharField(max_length=255, null=True, blank=True)
    artists = models.CharField(max_length=255, null=True, blank=True)

    venue = models.ForeignKey("Venue", on_delete=models.SET_NULL, null=True, blank=True)
    venue_override = tinymce_models.HTMLField(
        null=True,
        blank=True,
    )

    starttime = models.DateTimeField("Start time", null=True, db_index=True)
    starttime_override = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    # `description` will be presented as a tinymce field in the admin
    # because we're overriding `formfield_for_dbfield` in `EventAdmin`.
    # could use HMTLField from tinymce here too, probably, but stick with TextField
    # which we know works.
    description = models.TextField(null=True, blank=True)
    hyperlink = models.CharField(max_length=255, null=True, blank=True)  #

    # some events override the venue's age policy
    age_policy_override = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    age_policy_emoji_override = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    # same as `description` - this will be rich text
    preface = models.TextField(
        null=True,
        blank=True,
    )

    # optional hyperlink to tickets, separate from event.hyperlink value
    ticket_hyperlink = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    PRICE_RANGE = [
        ("$", "$"),
        ("$$", "$$"),
        ("$$$", "$$$"),
        ("$$$$", "$$$$"),
    ]
    price = models.CharField(
        max_length=255,
        choices=PRICE_RANGE,
        null=True,
        blank=True,
    )

    # will strikethrough most of the event information, except for the preface
    is_cancelled = models.BooleanField(default=False)

    same_time_order_override = models.IntegerField(verbose_name="Order", default=0)

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
    def age_policy_emoji(self):
        if self.age_policy_emoji_override:
            return self.age_policy_emoji_override
        if self.venue:
            return self.venue.age_policy_emoji
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
    # does the event have a 'the' as a prefix?
    # this is useful to keep separate for when we want to have an alphabetized list of venues
    # i.e. not have all of the 'the ...' venues all together
    name_the = models.BooleanField(default=False, verbose_name="the")
    address = models.CharField(max_length=255, null=True, blank=True)
    age_policy = models.CharField(max_length=255, null=True, blank=True)
    age_policy_emoji = models.CharField(max_length=255, null=True, blank=True)
    neighborhood_and_borough = models.CharField(max_length=255, null=True, blank=True)
    # convert this to urlfield for a bit more validation?
    # would have to check all existing values to be valid first..!
    google_maps_link = models.CharField(max_length=255, null=True, blank=True)
    accessibility_emoji = models.CharField(max_length=255, null=True, blank=True)
    accessibility_notes = models.TextField(null=True, blank=True)
    accessibility_link = models.CharField(max_length=255, null=True, blank=True)

    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cap = models.CharField(max_length=255, null=True, blank=True)
    hou$e = models.CharField(max_length=255, null=True, blank=True)
    booking_link = models.URLField(null=True, blank=True)
    backline_link = models.URLField(null=True, blank=True)



    def __str__(self):
        return f"{'the ' if self.name_the else ''}{self.name}"

    def full_name_with_the(self):
        return f"{'the ' if self.name_the else ''}{self.name}"


# custom manager that returns only public StaticPages by default
# so that most code (except for the admin) will do the right thing
# and show public pages only
class StaticPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)


class StaticPage(models.Model):
    objects = StaticPageManager()
    all_objects = models.Manager()

    is_public = models.BooleanField(default=True)

    url_path = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("static_page", kwargs={"url_path": self.url_path})

    def __str__(self):
        return self.title


class DateMessage(models.Model):
    date = models.DateField("Date", null=True)
    message = tinymce_models.HTMLField(null=True, blank=True)

    def __str__(self):
        return str(self.date)


class EmailSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class IndexPageMessages(SingletonModel):
    pre_cal_msg = tinymce_models.HTMLField(
        "Pre calendar message", null=True, blank=True
    )
    post_cal_msg = tinymce_models.HTMLField(
        "Post calendar message", null=True, blank=True
    )

    def __str__(self):
        return "Index Page Messages"

    class Meta:
        verbose_name = "Index Page Messages"


class MenuItem(OrderedModel):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    show_in_header = models.BooleanField(default=False)
    show_in_footer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
