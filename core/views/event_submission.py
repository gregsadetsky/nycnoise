from core.models import Event, Venue
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.views.generic.edit import CreateView


class DateTimePickerInput(forms.DateTimeInput):
    input_type = "datetime-local"


class UserSubmittedEventForm(forms.ModelForm):
    venue_override = forms.CharField(
        label=mark_safe("Venue Name<br>(if not in list above)"), required=False
    )
    venue = forms.models.ModelChoiceField(
        queryset=Venue.objects.filter(is_open=True), required=False
    )

    class Meta:
        model = Event
        fields = [
            "user_submission_email",
            "starttime",
            "hyperlink",
            "ticket_hyperlink",
            "title",
            "artists",
            "venue",
            "venue_override",
            "description",
            "price",
        ]
        labels = {"hyperlink": "Main Link", "ticket_hyperlink": "Ticket Link"}
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
        if data.get("venue") is None and venue_override.strip() == "":
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
