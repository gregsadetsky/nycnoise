# Generated by Django 4.2.5 on 2023-10-29 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0026_event_artists_alter_event_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="ticket_hyperlink",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
