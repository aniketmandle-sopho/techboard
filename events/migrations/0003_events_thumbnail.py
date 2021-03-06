# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-01 08:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('events', '0002_auto_20180124_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='thumbnail',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.Image'),
            preserve_default=False,
        ),
    ]
