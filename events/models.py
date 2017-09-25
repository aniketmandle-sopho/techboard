# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from django.db import models
from wagtail.wagtailsnippets.models import register_snippet

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock

	
# @register_snippet
# class EventLocation(models.Model):
# 	location = models.CharField(max_length=255)
# 	panels = [
# 		FieldPanel('location'),
# 	]

# 	def __str__(self):
# 		return self.location

# 	class Meta:
# 		verbose_name_plural = 'event locations'

# class LocationChooserBlock(blocks.ChooserBlock):
#     target_model = Tag
#     widget = forms.Select 

#     # Return the key value for the select field
#     def value_for_form(self, value):
#         if isinstance(value, self.target_model):
#             return value.pk
#         else:
#             return value

class Events(blocks.StructBlock):
	title = blocks.CharBlock()
	intro = blocks.RichTextBlock()
	start = blocks.DateTimeBlock()
	end = blocks.DateTimeBlock()
#	location = ParentalManyToManyField('events.EventLocation',blank=True)
	venue = blocks.CharBlock()
	isActive = blocks.BooleanBlock(required=False)


class EventIndexPage(Page):
	intro = RichTextField(max_length=250)
	event = StreamField([
		('evnt',Events()),

	])
	content_panels = Page.content_panels + [
		FieldPanel('intro'),
		StreamFieldPanel('event'),
	]
