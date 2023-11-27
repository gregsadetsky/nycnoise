# Generated by Django 4.2.5 on 2023-11-25 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0041_venue_name_the"),
    ]

    operations = [
        migrations.AddField(
            model_name="venue",
            name="age_policy_emoji",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="venue",
            name="name_the",
            field=models.BooleanField(default=False, verbose_name="the"),
        ),
    ]