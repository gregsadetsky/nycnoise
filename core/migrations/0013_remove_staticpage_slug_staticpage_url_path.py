# Generated by Django 4.2.5 on 2023-10-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_staticpage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staticpage",
            name="slug",
        ),
        migrations.AddField(
            model_name="staticpage",
            name="url_path",
            field=models.CharField(default="", max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
