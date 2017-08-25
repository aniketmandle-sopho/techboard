# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

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

# Create your models here.
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import IntegerBlock

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    clubname = models.CharField(max_length=30)
    rollno = models.PositiveIntegerField(default=1)
    phoneno = models.PositiveIntegerField(default=1)
    dp = models.ImageField()
    #bio = models.TextField(max_length=500, blank=True)
    #location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True)
    def __str__(self):
		content = "PROFILE_NAME : " + self.username
		return content

class Members(blocks.StructBlock):
    dp = ImageChooserBlock()
    name = blocks.CharBlock()
    rollno = blocks.IntegerBlock()
    phoneno = blocks.IntegerBlock()

   
class UserPage(Page):
    intro = RichTextField(max_length=250)
    members = StreamField([
        ('Members',Members()),

    ])
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('members'),
    ]


#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#       Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()