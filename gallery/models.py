# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

class GalleryPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class Album(Page):

	cover = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.CASCADE, related_name='+'
	) 
	body = StreamField([
        
		('image', ImageChooserBlock()),
		('video',EmbedBlock()),
	])
	content_panels = Page.content_panels + [
		ImageChooserPanel('cover'),    
		StreamFieldPanel('body'),
    ]