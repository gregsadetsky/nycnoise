# Generated by Django 4.2.5 on 2023-10-29 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0030_alter_event_venue"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="venue_override",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
