from core.models import Venue
from dal import autocomplete


def parse_venue_name(q):
    """
    Parse a venue name string that might have 'the' prefix.

    Args:
        q (str): Venue name string, possibly with 'the ' prefix

    Returns:
        tuple: (name, name_the) where:
            - name (str): The venue name without 'the' prefix if it existed
            - name_the (bool): Whether the original string had 'the' prefix
    """
    q = q.strip()

    # Check if query starts with 'the ' (case insensitive)
    if q.lower().startswith("the "):
        name = q[4:].strip()  # Remove 'the ' prefix (4 characters)
        return name, True
    else:
        return q, False


class VenueAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Venue.objects.filter(is_open=True)

        if not self.q:
            return qs

        name, name_the = parse_venue_name(self.q)

        if name_the:
            return qs.filter(name__icontains=name, name_the=True)
        return qs.filter(name__icontains=name)
