# Generated by Django 4.2.5 on 2023-10-23 18:36

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_merge_20231022_1915"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="venue",
            options={"ordering": [django.db.models.functions.text.Upper("name")]},
        ),
        migrations.AlterField(
            model_name="venue",
            name="location",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]