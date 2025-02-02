from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from taggit.models import TaggedItemBase
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField



class EventIndexPage(Page):
    body = RichTextField(blank=True)
    parent_page_types = ['home.HomePage']
    
    def get_context(self, request):
        context = super().get_context(request)
        eventpages = self.get_children().live().order_by('eventpage__date_on')
        context['eventpages'] = eventpages
        return context
    
    subpage_types = ['event.EventPage', 'event.EventTagIndexPage']
    parent_page_types = ['home.HomePage']

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Индексная страница событий (Афиша)"


class EventTagPage(TaggedItemBase):
    content_object = ParentalKey('EventPage', related_name='tegged_items', on_delete=models.CASCADE)
    

class EventPage(Page):
    date_on = models.DateField("Дата начала")
    date_end = models.DateField("Дата окончания", blank=True, null=True) # если указана, то это диапазон дат
    h1 = models.CharField('Заголовок', max_length=128)
    h2 = models.CharField('Подзаголовок', max_length=256, blank=True)
    body = RichTextField("Основная чвсть", blank=True)
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='+', help_text='Постер (1304x483)px, 2,7/1')
    tags = ClusterTaggableManager(through=EventTagPage, blank=True)
    founder = models.CharField('Организатор', max_length=256, blank=True)
    location = models.CharField('Место проведения', max_length=256, blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('h1'),
        index.SearchField('h2'),
        index.SearchField('body'),
        index.SearchField('founder'),
        index.SearchField('location'),
    ]
    
    subpage_types = ['base.FormPage']
    parent_page_types = ['event.EventIndexPage']

    api_fields = [
        APIField('date_on'),
        APIField('date_end'),
        APIField('h1'),
        APIField('h2'),
        APIField('body'),
        APIField('image'),
        APIField('image_thumbnail', serializer=ImageRenditionField('fill-380x220', source='image')),    # 19/11 соотношение картинки 380|290х..
        APIField('tags'),
        APIField('founder'),
        APIField('location'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('h1'),
        FieldPanel('image', heading="Изображение"),
        FieldPanel('tags'),
        FieldPanel('date_on'),
        FieldPanel('date_end'),
        FieldPanel('h2'),
        FieldPanel('body'),
        FieldPanel('founder'),
        FieldPanel('location'),
    ]
    
    class Meta:
        verbose_name = 'Событие'

    
    class EventTagIndexPage(Page):
        
        subpage_types = []
        parent_page_types = ['event.EventIndexPage']
        max_count = 1   # Всего одна страница тегов

        def get_context(self, requesst):
            tag = requesst.GET.get('tag')
            eventpages = EventPage.objects.live().filter(tags__name=tag)
            context = super().get_context(requesst)
            context['eventpages'] = eventpages
            return context

        subpage_types = []
        parent_page_types = ['home.HomePage']

        class Meta:
            verbose_name = 'Индекс тегов событий'
