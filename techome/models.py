from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index
from wagtail.wagtailembeds.blocks import EmbedBlock


class TechomePage(Page):

    # Database fields
    about_us    = RichTextField('about_us', blank=True)
    vision = RichTextField('vision', blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    related_links = StreamField([
        ('link', blocks.StructBlock([
            ('name', blocks.CharBlock(max_length=255)),
            ('url', blocks.URLBlock()),
        ])),
        ], blank = True)

    carousel = StreamField([
            #for images
        ('image', ImageChooserBlock()),
            # for quotes by people
        ('quotation', blocks.StructBlock([
            ('text', blocks.TextBlock()),
            ('author', blocks.CharBlock()),
        ])),
        # for video embedding
        ('video', EmbedBlock()),
        ],
        blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(TechomePage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('about_us', classname="full"),
        FieldPanel('vision', classname="full"),
        StreamFieldPanel('carousel'),
        StreamFieldPanel('related_links'),

    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]
