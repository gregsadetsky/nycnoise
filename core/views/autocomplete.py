from dal import autocomplete

from core.models import Venue


class VenueAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Venue.objects.filter(is_open=True)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
