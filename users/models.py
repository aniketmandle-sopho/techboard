# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

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
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	firstname = models.CharField(max_length=30)
	
	lastname = models.CharField(max_length=30)
	
	clubname_choices = (
		('automobile', 'Automobile'),
		('robotics', 'robotics'),
		('aeromodelling', 'aeromodelling'),
		('electronics', 'electronics'),
		('prakriti', 'prakriti'),
		('edc', 'EntrepreneurshipDevelopmentCell'),
		('fnc', 'FinanceandEconomics'),
		('coding', 'CodingClub'),
		('astronomy', 'Astronomy'),
		('acumen', 'Acumen'),
		('radiog', 'RadioG'),
	)

	clubname = models.CharField(
		max_length=20,
		choices=clubname_choices,
	)

	rollno = models.PositiveIntegerField(default=1)

	phoneno = models.PositiveIntegerField(default=1)

	display_picture = models.ImageField()

	birth_date = models.DateField(null=True)

	def __str__(self):
		content = self.firstname + " " +self.lastname
		return content


   
class UserPage(Page):
	intro = RichTextField(max_length=250)
	
	clubname_choices = (
		('automobile', 'Automobile'),
		('robotics', 'robotics'),
		('aeromodelling', 'aeromodelling'),
		('electronics', 'electronics'),
		('prakriti', 'prakriti'),
		('edc', 'EntrepreneurshipDevelopmentCell'),
		('fnc', 'FinanceandEconomics'),
		('coding', 'CodingClub'),
		('astronomy', 'Astronomy'),
		('acumen', 'Acumen'),
		('radiog', 'RadioG'),
	)

	clubname = models.CharField(
		max_length=20,
		choices=clubname_choices,
	)

	def get_context(self, request):
		members = []    
		context = super(UserPage, self).get_context(request)
		users = User.objects.all()
		for user in users:
			if(user.profile.clubname == self.clubname):                
				members.append(user)
		context['members'] = members
		return context

	content_panels = Page.content_panels + [
		FieldPanel('intro'),
		FieldPanel('clubname'),
	]

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#       Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()