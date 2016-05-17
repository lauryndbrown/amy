# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-17 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0089_renaming_column_tag_changes_detected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='metadata_all_changes',
            field=models.TextField(blank=True, default='', help_text='List of detected metadata changes'),
        ),
    ]
