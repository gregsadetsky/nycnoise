from django import forms
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from core.models import Event


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class UserSubmittedEventForm(forms.ModelForm):
    venue_override = forms.CharField(
        label="Venue Name (if you can't find in list above)",
        required=False
    )

    class Meta:
        model = Event
        fields = [
            "starttime",
            "hyperlink",  # change name to "main link"
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


class EventCreateView(CreateView):
    model = Event
    form_class = UserSubmittedEventForm

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_approved = False
        obj.user_submitted = True
        obj.save()
        return HttpResponseRedirect(self.get_success_url())
