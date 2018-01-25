# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index
from events import models as event
from django.db.models import Q
from django import forms
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from story.models import StoryPage, StoryIndexPage



class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    caption = blocks.TextBlock()

    class Meta:
        icon='cogs'

        

class ClubHomePage(Page):
	slideshow = StreamField(
		[ ('Image', CaptionedImageBlock()) ], 
		blank=True)

	about_us = RichTextField(blank=True)
	
	vision = RichTextField(blank=True)
	
	facebook = models.CharField(max_length=200,default='')	 
	
	googleplus = models.CharField(blank=True,max_length=200)	 
	
	twitter = models.CharField(blank=True,max_length=200)	 
	
	youtube = models.CharField(blank=True, max_length=200)	 
	
	email = models.CharField(max_length=200,default='')

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('facebook'),
			FieldPanel('googleplus'),
			FieldPanel('twitter'),
			FieldPanel('youtube'),
			FieldPanel('email'),
		], heading='Contact Links'),
		StreamFieldPanel('slideshow'),
		FieldPanel('about_us'),
		FieldPanel('vision'),
	]

	subpage_types = ['achievements.AchievementsIndexPage','gallery.GalleryPage','projects.ProjectsPage','story.StoryIndexPage','story.StoryTagIndexPage','events.EventIndexPage','users.UserPage']

	def get_context(self, request):
		# Update context to include only published posts, ordered by reverse-chron
		context = super(ClubHomePage, self).get_context(request)
		eveindpag = self.get_children().live().type(event.EventIndexPage)
		aevent = event.Events.objects.filter(Q(page=eveindpag)&Q(is_active=1)).order_by('start')[:1]
		context['aevent'] = aevent
		stindpag = self.get_children().live().type(StoryIndexPage).first()
		if stindpag is not None:
			astory = stindpag.get_children().live().order_by('-first_published_at')[:1]
			context['astory'] = astory
		return context