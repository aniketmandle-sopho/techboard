from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet
from django.db.models import Q
from django import forms
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from story.models import StoryPage, StoryIndexPage
from events.models import Events



class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    caption = blocks.TextBlock()

    class Meta:
        icon='cogs'



class HomePage(Page):
    slideshow = StreamField(
        [ ('Image',CaptionedImageBlock()) ] , 
        blank=True)

    about_us = RichTextField(blank=True)
    tagline = models.CharField(max_length=200, blank = True)
    vision = RichTextField(blank=True)

    facebook = models.CharField(max_length=200,default='')  

    googleplus = models.CharField(blank=True,max_length=200)    

    twitter = models.CharField(blank=True,max_length=200)   

    youtube = models.CharField(blank=True, max_length=200)  

    email = models.CharField(max_length=200,default='')

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

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
        FieldPanel('tagline'),
        FieldPanel('vision'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]
    
    subpage_types = ['club_home.ClubHomePage','story.StoryTagIndexPage']

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(HomePage, self).get_context(request)
        aevent = Events.objects.filter(Q(is_active=1)).order_by('start')[:6]
        context['aevent'] = aevent
        return context