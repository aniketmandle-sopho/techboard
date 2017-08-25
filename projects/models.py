# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

class ProjectsPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(ProjectsPage, self).get_context(request)
        projects = self.get_children().live().order_by('-first_published_at')
        context['projects'] = projects
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    subpage_types = ['projects.Projects']

class Projects(Page):
	
	
	start = models.DateField("startdate")
	end = models.DateField("enddate")
	body = StreamField([
        
        ('Descrip', blocks.RichTextBlock()),
        ('Images', ImageChooserBlock()),
        ('Link', blocks.URLBlock()),
        ('Documents',DocumentChooserBlock()),
        ('video',EmbedBlock()),
        ('Gist',blocks.RichTextBlock()),

    ])

	content_panels = Page.content_panels + [
    	
        FieldPanel('start'),
        FieldPanel('end'),
        StreamFieldPanel('body'),
    ]