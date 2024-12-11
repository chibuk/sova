from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from taggit.models import TaggedItemBase
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager



class EventIndexPage(Page):
    body = RichTextField(blank=True)
    
    def get_context(self, request):
        context = super().get_context(request)
        eventpages = self.get_children().live().order_by('-first_publishd_at')
        context['eventpages'] = eventpages
        return context
    
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class EventTagPage(TaggedItemBase):
    content_object = ParentalKey('EventPage', related_name='tegged_items', on_delete=models.CASCADE)
    

class EventPage(Page):
    date_on = models.DateField("Дата начала")
    date_end = models.DateField("Дата окончания", blank=True) # если указана, то это диапазон дат
    h1 = models.CharField('Заголовок', max_length=128, blank=True)
    h2 = models.CharField('Подаголовок', max_length=256, blank=True)
    body = RichTextField("Основная чвсть", blank=True)
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='+', help_text='Постер (1360x544)px, 2,5/1')
    tags = ClusterTaggableManager(through=EventTagPage, blank=True)
    founder = models.CharField('Организатор', max_length=256, blank=True)
    place = models.CharField('Место проведения', max_length=256, blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('h1'),
        index.SearchField('h2'),
        index.SearchField('body'),
        index.SearchField('founder'),
        index.SearchField('place'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('date_on'),
        FieldPanel('date_end'),
        FieldPanel('h1'),
        FieldPanel('h2'),
        FieldPanel('body'),
        FieldPanel('image'),
        FieldPanel('tags'),
        FieldPanel('founder'),
        FieldPanel('place'),
    ]
    
    
    class EventTagIndexPage(Page):
        
        def get_context(self, requesst):
            tag = requesst.GET.get('tag')
            eventpages = EventPage.objects.live().filter(tags__name=tag)
            context = super().get_context(requesst)
            context['eventpages'] = eventpages
            return context
