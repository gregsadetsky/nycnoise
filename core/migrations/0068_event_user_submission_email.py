# Generated by Django 4.2.10 on 2024-03-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0067_remove_venue_closed"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="user_submission_email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
