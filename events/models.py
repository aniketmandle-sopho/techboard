# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from django.db import models
from wagtail.wagtailsnippets.models import register_snippet

# Create your models here.
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel
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
from django.db.models import Q
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

class EventIndexPage(Page):
	intro = RichTextField(max_length=250)
	def get_context(self, request):
		# Update context to include only published posts, ordered by reverse-chron
		context = super(EventIndexPage, self).get_context(request)
		active_events = Events.objects.filter(Q(page=self)&Q(IsActive=1)).order_by('start')
		context['active_events'] = active_events
		inactive_events = Events.objects.filter(Q(page=self)&Q(IsActive=0)).order_by('-end')
		context['inactive_events'] = inactive_events
		return context


	content_panels = Page.content_panels + [
		FieldPanel('intro'),
		InlinePanel('events', label="Event"),
	]

class Events(Orderable):
	page = ParentalKey(EventIndexPage, related_name='events')
	title = models.CharField(max_length=200)
	intro = RichTextField()
	start = models.DateTimeField("Start")
	end = models.DateTimeField("end")
	venue = models.CharField(max_length=200)
	IsActive = models.BooleanField(blank=True,default=True)

#	location = ParentalManyToManyField('events.EventLocation',blank=True)
	panels = [
		FieldPanel('IsActive'),
		FieldPanel('title'),
        FieldPanel('intro'),
        MultiFieldPanel([
	        FieldPanel('start'),
	        FieldPanel('end'),
	        FieldPanel('venue'),
    	],heading='Details Of Event')
    ]