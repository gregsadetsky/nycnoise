# Generated by Django 4.2.5 on 2023-10-29 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0031_event_venue_override"),
    ]

    operations = [
        migrations.RenameField(
            model_name="venue",
            old_name="location",
            new_name="address",
        ),
    ]
