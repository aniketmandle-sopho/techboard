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
from django.db.models import Q
from story.models import StoryPage, StoryIndexPage

from events.models import Events
from django.db.models import Q
class ImagecBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.TextBlock()

    class Meta:
        icon='cogs'

class HomePage(Page):
    slideshow = StreamField([
        ('Image',ImagecBlock()),

    ], blank=True)

    AboutUs = RichTextField(blank=True)
    Vision = RichTextField(blank=True)
    facebook_link = models.CharField(max_length=200,default='')  
    googleplus_link = models.CharField(blank=True,max_length=200)    
    twitter_link = models.CharField(blank=True,max_length=200)   
    youtube_link = models.CharField(blank=True, max_length=200)  
    emailaddress = models.CharField(max_length=200,default='')

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(HomePage, self).get_context(request)
        aevent = Events.objects.filter(Q(IsActive=1)).order_by('start')[:4]
        context['aevent'] = aevent
        return context
    # Database fields

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('facebook_link'),
            FieldPanel('googleplus_link'),
            FieldPanel('twitter_link'),
            FieldPanel('youtube_link'),
            FieldPanel('emailaddress'),
        ], heading='Contact Links'),
        StreamFieldPanel('slideshow'),
        FieldPanel('AboutUs'),
        FieldPanel('Vision'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]
    
    subpage_types = ['club_home.ClubHomePage','story.StoryTagIndexPage']
