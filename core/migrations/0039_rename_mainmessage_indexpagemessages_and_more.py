# Generated by Django 4.2.5 on 2023-11-25 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0038_alter_mainmessage_post_cal_msg_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="MainMessage",
            new_name="IndexPageMessages",
        ),
        migrations.AlterModelOptions(
            name="indexpagemessages",
            options={"verbose_name": "Index Page Messages"},
        ),
    ]
