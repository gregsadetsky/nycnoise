# Generated by Django 4.2.10 on 2024-02-17 20:14

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0059_searchablestaticpagebit"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="searchablestaticpagebit",
            name="search_vector_idx",
        ),
        migrations.AddField(
            model_name="searchablestaticpagebit",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(
                editable=False, null=True
            ),
        ),
        migrations.AddIndex(
            model_name="searchablestaticpagebit",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="core_search_search__c68fc3_gin"
            ),
        ),
    ]