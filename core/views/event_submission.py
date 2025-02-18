from core.models import Event, Venue
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.html import escape, mark_safe
from django.views.generic.edit import CreateView

from dal import autocomplete


class DateTimePickerInput(forms.DateTimeInput):
    input_type = "datetime-local"


class UserSubmittedEventForm(forms.ModelForm):
    template_name = "core/event_form_fields.html"

    venue = forms.models.ModelChoiceField(
        label="venue",
        queryset=Venue.objects.filter(is_open=True),
        required=False,
        widget=autocomplete.ModelSelect2(url='venue-autocomplete/')
    )
    # description = forms.CharField()
    # description = forms.Textarea(rows=4)

    class Meta:
        model = Event
        fields = [
            "starttime",
            "hyperlink",
            "title",
            "artists",
            "venue",
            "ticket_hyperlink",
            "price",
            "user_submission_email",
        ]
        labels = {
            "hyperlink": "main link",
            "ticket_hyperlink": "ticket link",
            "user_submission_email": "yr email",
            "starttime": "date + time",
            "hyperlink": "link",
            "title": mark_safe("title (if any)"),
            "ticket_hyperlink": "ticket link",
            "artists": "artists",
            "price": "price",
        }
        widgets = {
            "starttime": DateTimePickerInput(),
        }

    def save(self, commit=True):
        """user-submitted events will always be unapproved"""
        obj = super().save(commit=False)

        # de-claw the description
        obj.description = escape(obj.description)

        obj.is_approved = False
        obj.user_submitted = True
        if commit:
            obj.save()
        return obj

    def clean(self):
        data = super().clean()
        if data.get("title") is None and data.get("artists") is None:
            raise ValidationError("event must include title or artists")
        venue_override = data.get("venue_override")
        if data.get("venue") is None:
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
