# Generated by Django 4.2.8 on 2023-12-17 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0048_alter_event_starttime"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="age_policy_emoji_override",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]