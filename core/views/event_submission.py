from core.models import Event, Venue
from dal import autocomplete
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.html import escape, mark_safe
from django.views.generic.edit import CreateView


class DateTimePickerInput(forms.DateTimeInput):
    input_type = "datetime-local"


class UserSubmittedEventForm(forms.ModelForm):
    template_name = "core/event_form_fields.html"

    venue = forms.models.ModelChoiceField(
        label="venue",
        queryset=Venue.objects.filter(is_open=True),
        required=False,
        widget=autocomplete.ModelSelect2(url="venue-autocomplete/"),
    )

    # to get url validation/input type=url on the frontend
    hyperlink = forms.URLField(label="link", required=False)
    ticket_hyperlink = forms.URLField(label="ticket link", required=False)

    class Meta:
        model = Event
        fields = [
            "user_submission_email",
            "starttime",
            "hyperlink",
            "title",
            "artists",
            "venue",
            "price",
            "ticket_hyperlink",
            "description",
        ]
        labels = {
            "user_submission_email": "yr email",
            "starttime": "date + time",
            "hyperlink": "link",
            "title": mark_safe("<i>(optional)</i> title"),
            "ticket_hyperlink": "ticket link",
            "artists": "artists",
            "price": "price",
            "description": "extra info (e.g., venue if not in drop-down)"
        }
        widgets = {
            "starttime": DateTimePickerInput(),
        }

    def save(self, commit=True):
        """user-submitted events will always be unapproved"""
        obj = super().save(commit=False)
        obj.is_approved = False
        obj.user_submitted = True
        if commit:
            obj.save()
        return obj

    def clean(self):
        data = super().clean()

        # escape all text-based fields
        text_fields = ["title", "artists", "description", "venue_override"]
        for field in text_fields:
            if data.get(field):
                data[field] = escape(data[field])

        if data.get("title") is None and data.get("artists") is None:
            raise ValidationError("event must include title or artists")

        venue_override = data.get("venue_override")
        venue = data.get("venue")
        if venue is None and (venue_override is None or venue_override.strip() == ""):
            raise ValidationError("event must contain some venue information")


class EventCreateView(CreateView):
    model = Event
    form_class = UserSubmittedEventForm

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.INFO,
            "thanks buddy! your event is submitted for approval.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return "/"
