# Generated by Django 4.2.5 on 2023-10-09 20:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_event_starttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 9, 20, 49, 47, 359483, tzinfo=datetime.timezone.utc), verbose_name='Start time'),
        ),
    ]
