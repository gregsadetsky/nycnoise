# Generated by Django 4.2.8 on 2023-12-17 20:45

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0050_auto_20231217_1539"),
    ]

    operations = [
        migrations.AddField(
            model_name="venue",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="venue",
            name="phone",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="venue",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="venue_override",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
