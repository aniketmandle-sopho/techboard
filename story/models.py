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






class StoryIndexPage(Page):
    intro = RichTextField(blank=True)
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(StoryIndexPage, self).get_context(request)
        storypages = self.get_children().live().order_by('-first_published_at')
        context['storypages'] = storypages
        return context
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
class StoryPageTag(TaggedItemBase):
    content_object = ParentalKey('StoryPage', related_name='tagged_items')


class StoryPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, help_text="Listen up buddy This thing is non editable Yeah!")
    author = models.CharField(max_length=250,default="Anonymous")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
		('images', blocks.StructBlock(
		    [
		        ('image', ImageChooserBlock()),
		        
		        ('caption', blocks.CharBlock()),
		    ],
		    icon='image',
		)),
		('gist', blocks.TextBlock(help_text="Go to gist.github.com to write code and copy the embed Link.")),
        ('link', blocks.URLBlock()),
        ('quote',blocks.BlockQuoteBlock()),
        ('embed',EmbedBlock()),
    ])
    tags = ClusterTaggableManager(through=StoryPageTag, blank=True)
    
    categories = ParentalManyToManyField('story.StoryCategory', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
    	MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('author'),
            FieldPanel('tags'),

            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Information About Story"),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]


class StoryTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        storypages = StoryPage.objects.filter(tags__name=tag)

        # Update template context
        context = super(StoryTagIndexPage, self).get_context(request)
        context['storypages'] = storypages
        return context

@register_snippet
class StoryCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'story categories'