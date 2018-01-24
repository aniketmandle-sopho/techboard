# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField,StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock



class ProjectsPage(Page):
	intro = RichTextField(blank=True)

	content_panels = Page.content_panels + [
		FieldPanel('intro', classname="full")
	]

	subpage_types = ['projects.Projects']

	def get_context(self, request):
		# Update context to include only published posts, ordered by reverse-chron
		context = super(ProjectsPage, self).get_context(request)
		projects = self.get_children().live().order_by('-first_published_at')
		context['projects'] = projects
		return context



class Projects(Page):
	start = models.DateField("startdate")

	end = models.DateField("enddate",help_text="If ongoing leave blank.",blank=True,null=True)
	
	intro = models.CharField(help_text="This is the context which will be in Main Projects Page",max_length=600)
	
	body = StreamField([
		('Descrip', blocks.RichTextBlock()),
		('Images', ImageChooserBlock()),
		('Link', blocks.StructBlock(
			[
				('URL', blocks.URLBlock()),
				
				('Text', blocks.CharBlock()),
			],
			icon='site',
		)),
		('Documents',DocumentChooserBlock()),
		('video',EmbedBlock()),
		('Gist',blocks.TextBlock()),
	])

	content_panels = Page.content_panels + [
		FieldPanel('intro'),
		MultiFieldPanel([
			FieldPanel('start'),
			FieldPanel('end'),
		],heading='Dates Of Project'),
		StreamFieldPanel('body'),
	]