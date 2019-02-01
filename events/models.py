# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailsearch import index
from django.db.models import Q
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase



class EventIndexPage(Page):
	intro = RichTextField(max_length=250)


	def get_context(self, request):
		# Update context to include only published posts, ordered by reverse-chron
		context = super(EventIndexPage, self).get_context(request)
		active_events = Events.objects.filter(Q(page=self)&Q(is_active=1)).order_by('start')
		context['active_events'] = active_events
		inactive_events = Events.objects.filter(Q(page=self)&Q(is_active=0)).order_by('-end')
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
	thumbnail = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.PROTECT, related_name='+'
	) 
	venue = models.CharField(max_length=200)

	is_active = models.BooleanField(blank=True,default=True)

	panels = [
		FieldPanel('is_active'),
		FieldPanel('title'),
        FieldPanel('intro'),
        FieldPanel('thumbnail'),
        MultiFieldPanel([
	        FieldPanel('start'),
	        FieldPanel('end'),
	        FieldPanel('venue'),
    	],heading='Details Of Event')
    ]