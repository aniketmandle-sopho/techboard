from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index
from wagtail.wagtailembeds.blocks import EmbedBlock


class AchievementsIndexPage(Page):
    intro = RichTextField(blank=True)
    author = models.CharField(max_length=255, blank=True)
    carousel = StreamField([
        ('image', ImageChooserBlock()),
        ('quotation', blocks.StructBlock([
            ('text', blocks.TextBlock()),
            ('author', blocks.CharBlock()),
        ])),
        ('video', EmbedBlock()),
        ],
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('author'),
        StreamFieldPanel('carousel'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(AchievementsIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
    subpage_types = ['achievements.AchievementsPage']

class AchievementsPage(Page):
    date = models.DateField("Post date")
    competition_intro = RichTextField("About the Achievement")
    description = RichTextField("Descriptopn")

    carousel = StreamField([
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock()),
        ],
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('competition_intro'),
        FieldPanel('description', classname="full"),
        StreamFieldPanel('carousel'),

    ]
    parent_page_types = ['achievements.AchievementsIndexPage']
