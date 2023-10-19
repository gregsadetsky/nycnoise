from django.db import models

from tinymce import models as tinymce_models

class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey("Venue", on_delete=models.PROTECT)
    starttime = models.DateTimeField("Start time", null=True)
    description = tinymce_models.HTMLField(max_length=1000, null=True, blank=True)

    def gcal_link(self):
        # example link
        # https://www.google.com/calendar/render?action=TEMPLATE&text=Your+Event+Name&dates=20140127T224000Z/20140320T221500Z&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022&sf=true&output=xml
        start_hour = self.starttime.hour
        end_hour = (self.starttime.hour + 1) % 24
        date_start = f'{self.starttime.date().isoformat().replace("-", "")}T{start_hour}{self.starttime.minute}00Z'
        date_end = f'{self.starttime.date().isoformat().replace("-", "")}T{end_hour}{self.starttime.minute}00Z'
        gcal_link = f'https://www.google.com/calendar/render?action=TEMPLATE'
        gcal_link += f'&text={self.name.replace(" ", "+")}'
        gcal_link += f'&dates={date_start}/{date_end}'
        gcal_link += f'&details={self.description.replace(" ", "+")}'
        gcal_link += f'&location={self.venue.location.replace(" ", "+")}'
        gcal_link += '&sf=true&output=xml'
        return gcal_link

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
