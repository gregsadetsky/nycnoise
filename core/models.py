from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models.functions import Upper
from django.urls import reverse
from ordered_model.models import OrderedModel
from solo.models import SingletonModel
from tinymce import models as tinymce_models

from core.utils_event_caching import bake_event_html
from core.utils_static_page import refresh_searchable_static_page_bits


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_approved=True)


class Event(models.Model):
    # the ORDER of these i.e. objects first, then all_objects, matters........!!!!!
    # I initially thought that overriding a manager meant
    # that the admin classes would need to have a custom get_queryset,
    # but it's trickier than that... yes, you CAN define a get_queryset for the admin
    # of a class with a custom manager, but that will break in very subtle ways --
    # for example, the `list_editable` property in the EventAdmin class which lets
    # us edit the `order` field directly in the list view will NOT take into account
    # the get_queryset... actually, I don't know what it takes into account...
    # it just DOESN'T WORK AT ALL....!!! is there an update_queryset...?? I didn't find
    # anything in the docs...... anyway, the admin class does take into the account the
    # first encountered manager in the model class i.e. here, i.e. Event. more info:
    # https://docs.djangoproject.com/en/4.2/topics/db/managers/#default-managers
    # (note, again, that somehow all_objects was interfering with list_editable regardless...)
    # ~
    # I ALSO found out that get_object_or_404 also uses the first-found-manager
    # which, if you use all_objects as the first manager (wanting to fix the admin
    # list_editable problem), you'll then have to manually change all of the
    # get_object_or_404 calls to be passed the .objects manager... and never forget to do
    # that anywhere else... extremely annoying.
    # ~
    # SO, in the end I decided to use the narrowed-manager .objects as the first (in order)
    # manager in both Event and Static AND to use a truly baroque AllEventProxy class
    # (see below) that is then used in the admin for all events... this makes it possible
    # to not have a get_queryset in the admin AND list_editable works...
    objects = EventManager()
    all_objects = models.Manager()

    # title and artists are separate fields
    # when both are present, title will be not bold and artists will be bold
    # when either are present, whichever is present will be shown in bold
    title = models.CharField(max_length=255, null=True, blank=True)
    artists = models.CharField(max_length=255, null=True, blank=True)

    # user-submitted events will not be included in the event calendar until
    # they are approved by an admin.
    user_submitted = models.BooleanField(default=False)
    is_approved = models.BooleanField(
        default=True
    )  # set to false in the submission view
    user_submission_email = models.EmailField(
        null=True,
        blank=True,
    )

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
        ("🌀 free", "🌀 free"),
        ("🌀 notaflof", "🌀 notaflof"),
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

    baked_html_template = models.TextField(null=True, blank=True)

    @property
    def get_baked_html(self):
        if not self.baked_html_template:
            self.rebake_html()
        return self.baked_html_template

    def rebake_html(self):
        self.baked_html_template = bake_event_html(self)
        self.save()

    def save(self, *args, **kwargs):
        # save contents - just to be sure that object data is not 'floating'
        # and is actually accessible by template rendering
        super().save(*args, **kwargs)

        # rebake html, store/save it.
        # the below is 10000000000000000000000000000000% not kosher, but
        # I couldn't immediately figure out how to call super().save() a second time
        # without the whole orm freaking out and saying (when an object was being created)
        # that a duplicate id was being inserted.
        # ((probably because the object is considered as being-created and has no pk,
        # and the second super().save call also tries to initialize the pk...?))
        # https://stackoverflow.com/questions/31187359/django-save-method-needs-to-update-model-instance-twice#comment50382190_31187599
        baked_html_template = bake_event_html(self)
        Event.objects.filter(pk=self.pk).update(baked_html_template=baked_html_template)

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


# this ONLY exists for admin purposes and dealing with the problem
# of the list_editable field `order` not working (i.e. changes to it not being saved)
# when using a custom manager on the Event class (i.e. all_objects & objects)
# AND using a get_queryset on the admin class to be able to edit all objects......!
# because that combo doesn't work, we use a proxy model class (AllEventProxy)
# and configure the admin class to use that instead of the original Event class.
# see https://stackoverflow.com/a/54471299
class AllEventProxy(Event):
    class Meta:
        verbose_name = Event._meta.verbose_name
        verbose_name_plural = Event._meta.verbose_name_plural
        proxy = True

    # this will be the 'default manager' used in the Admin, and elsewhere
    objects = models.Manager()


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
    accessibility_emoji = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="♿️"
    )
    accessibility_notes = tinymce_models.HTMLField(null=True, blank=True)
    accessibility_link = models.CharField(max_length=255, null=True, blank=True)

    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    is_open = models.BooleanField(default=True)

    capacity = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="cap"
    )
    house_fees = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="fees"
    )
    booking_link = models.URLField(null=True, blank=True)
    backline_link = models.URLField(null=True, blank=True)

    wage_information = tinymce_models.HTMLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # actually save data to db
        super().save(*args, **kwargs)
        # for all related events, refresh their baked html
        for event in self.event_set.all():
            event.rebake_html()

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
    # the ORDER of all_objects and THEN objects matters.
    # see larger discussion in the Event model class to see why/how.
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        refresh_searchable_static_page_bits(
            self,
            delete_only=not self.is_public,
        )


# StaticPage's content fields are too long to be indexed by postgres,
# which leads to super slow search (which we had to remove after the site launch).
# SearchableStaticPageBit stores overlapping split up 'bits' of content
# which can be indexed and will relate back to the original static page they came from
class SearchableStaticPageBit(models.Model):
    # models.CASCADE takes care of deleting the searchable bits when a static page is deleted
    static_page = models.ForeignKey(StaticPage, on_delete=models.CASCADE)
    content_text_extract = models.TextField()
    # see https://stackoverflow.com/a/70812950
    search_vector = SearchVectorField(editable=False, null=True)

    class Meta:
        # The search index pointing to our actual search field.
        indexes = [GinIndex(fields=["search_vector"])]


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
