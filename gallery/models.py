# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailembeds.blocks import EmbedBlock



class GalleryPage(Page):
	intro = RichTextField(blank=True)

	content_panels = Page.content_panels + [FieldPanel('intro', classname="full")]
	
	subpage_types = ['gallery.Album']

	def get_context(self, request):
		context = super(GalleryPage, self).get_context(request)
		albums = self.get_children().live().order_by('-first_published_at')
		context['albums'] = albums
		return context



class Album(Page):
	cover = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.PROTECT, related_name='+'
	) 

	desc = RichTextField(blank=True)

	body = StreamField([
		('image', ImageChooserBlock()),
		('video',EmbedBlock()),
	])

	content_panels = Page.content_panels + [
		FieldPanel('desc', classname="full"),
		ImageChooserPanel('cover'),    
		StreamFieldPanel('body'),
	]