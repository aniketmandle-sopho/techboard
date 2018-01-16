# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-16 14:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0039_collectionviewrestriction'),
    ]

    operations = [
        migrations.CreateModel(
            name='AchievementsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('author', models.CharField(blank=True, max_length=255)),
                ('carousel', wagtail.wagtailcore.fields.StreamField([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'quotation', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.TextBlock()), (b'author', wagtail.wagtailcore.blocks.CharBlock())])), (b'video', wagtail.wagtailembeds.blocks.EmbedBlock())], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AchievementsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(verbose_name=b'Post date')),
                ('competition_intro', models.CharField(max_length=600, verbose_name=b'About the Achievement')),
                ('description', wagtail.wagtailcore.fields.RichTextField(verbose_name=b'Decription')),
                ('carousel', wagtail.wagtailcore.fields.StreamField([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'video', wagtail.wagtailembeds.blocks.EmbedBlock())], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
