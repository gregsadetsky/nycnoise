# Generated by Django 4.2.9 on 2024-02-17 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0056_alter_event_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="price",
            field=models.CharField(
                blank=True,
                choices=[
                    ("🌀 free", "🌀 free"),
                    ("🌀 notaflof", "🌀 notaflof"),
                    ("$", "$"),
                    ("$$", "$$"),
                    ("$$$", "$$$"),
                    ("$$$$", "$$$$"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]