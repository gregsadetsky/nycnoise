# Generated by Django 4.2.5 on 2023-10-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0027_event_ticket_hyperlink"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="price",
            field=models.CharField(
                blank=True,
                choices=[("$", "$"), ("$$", "$$"), ("$$$", "$$$"), ("$$$$", "$$$$")],
                max_length=255,
                null=True,
            ),
        ),
    ]