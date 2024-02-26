from django import forms
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.core.exceptions import ValidationError

from core.models import Event


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class UserSubmittedEventForm(forms.ModelForm):
    venue_override = forms.CharField(
        label="Venue Name (if not in list above)",
        required=False
    )

    class Meta:
        model = Event
        fields = [
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
        labels = {
            "hyperlink": "Main Link",
            "ticket_hyperlink": "Ticket Link"
        }
        widgets = {
            'starttime': DateTimePickerInput(),
            'freeform_venue_name': DateTimePickerInput()
        }

    def save(self, commit=True):
        """ user-submitted events will always be unapproved """
        obj = super().save(commit=False)
        obj.is_approved = False
        obj.user_submitted = True
        if commit:
            obj.save()
        return obj

    def clean(self):
        data = super().clean()
        if data.get('title') is None and data.get('artists') is None:
            raise ValidationError('event must include title or artists')
        override = data.get('venue_override')
        if data.get('venue') is None and (override == '' or override.isspace()):
            raise ValidationError('event must contain some venue information')


class EventCreateView(CreateView):
    model = Event
    form_class = UserSubmittedEventForm

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.INFO,
            'Thanks buddy! Your event is submitted for approval.')
        return super().form_valid(form)

    def get_success_url(self):
        return '/'
