# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from django import forms



class StoryIndexPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['story.StoryPage']

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(StoryIndexPage, self).get_context(request)
        storypages = self.get_children().live().order_by('-first_published_at')
        context['storypages'] = storypages
        context['random'] = 1511
        return context



class StoryPageTag(TaggedItemBase):
    content_object = ParentalKey('StoryPage', related_name='tagged_items')



class StoryPage(Page):
    date = models.DateField("Post date")

    intro = models.CharField(max_length=250)
    # intro = models.CharField(max_length=250, help_text="Listen up buddy This thing is non editable Yeah!")
    
    author = models.CharField(max_length=250,default="Anonymous")
    
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
		('images', blocks.StructBlock(
		    [
		        ('image', ImageChooserBlock()),
		        
		        ('caption', blocks.CharBlock(blank=True,required=False,null=True)),
		    ],
		    icon='image',
		)),
		('gist', blocks.TextBlock(help_text="Go to gist.github.com to write code and copy the embed Link.")),
        ('Link', blocks.StructBlock(
            [
                ('URL', blocks.URLBlock()),
                
                ('Text', blocks.CharBlock()),
            ],
            icon='site',
        )),
        ('Quote',blocks.StructBlock(
            [
                ('quote',blocks.BlockQuoteBlock()),
                ('Author',blocks.TextBlock(max_length=50)),
            ],
            icon='quote'
        )),
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