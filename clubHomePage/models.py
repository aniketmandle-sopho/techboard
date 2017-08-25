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
from events import models

class ImagecBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.TextBlock()

    class Meta:
        icon='cogs'

class clubHomePage(Page):
	slideshow = StreamField([
		('Image',ImagecBlock()),

	], blank=True)

	AboutUs = RichTextField(blank=True)
	Vision = RichTextField(blank=True)
	 
	def get_context(self, request):
		# Update context to include only published posts, ordered by reverse-chron
		context = super(clubHomePage, self).get_context(request)
		aevent = self.get_children().live().type(models.EventIndexPage)
		context['aevent'] = aevent
		return context

	content_panels = Page.content_panels + [
		StreamFieldPanel('slideshow'),
		FieldPanel('AboutUs'),
		FieldPanel('Vision'),
	]
	subpage_types = ['achievements.AchievementsIndexPage','gallery.GalleryPage','projects.ProjectsPage','story.StoryIndexPage','events.EventIndexPage','users.UserPage']
