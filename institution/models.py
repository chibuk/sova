'''
Учреждения
'''
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey


class InstitutionPage(Page):
    name = models.CharField('Наименование', max_length=512)
    logo = models.ForeignKey('wagtailimages.Image', null=True, blank=True, verbose_name="Логотип",
                                   on_delete=models.SET_NULL, related_name='+', help_text='Логотип')
    description = RichTextField('Описание', blank=True)
    site = models.CharField('Сайт', max_length=512, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('description'),
    ]
    subpage_types = ['institution.TrainerIndexPage']
    parent_page_types = ['institution.InstitutionIndexPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('description'),
        FieldPanel('site'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        pages = self.get_children().live()
        context['indexpages'] = pages
        return context


class InstitutionIndexPage(Page):
    body = RichTextField(blank=True)
    
    parent_page_types = ['home.HomePage']
    
    def get_context(self, request):
        context = super().get_context(request)
        pages = self.get_children().live().order_by('institutionpage__name')
        context['institutionpages'] = pages
        return context
    
    subpage_types = ['institution.InstitutionPage']
    
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class TrainerPage(Page):
    surname = models.CharField('Фамилия', max_length=64)
    name = models.CharField('Имя', max_length=64)
    name2 = models.CharField('Отчество', max_length=64, null=True, blank=True)
    foto = models.ForeignKey('wagtailimages.Image', null=True, blank=True, verbose_name="Фото",
                                   on_delete=models.SET_NULL, related_name='+', help_text='Фотография')
    birth = models.DateField('Дата рождения', blank=True, null=True)
    education = models.CharField('Образование', max_length=128, null=True, blank=True)
    ranks = models.CharField('Звания и достижения', max_length=128, null=True, blank=True)
    # category = тренерская катергория со сроком действия

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('surname'),
    ]
    subpage_types = []
    parent_page_types = ['institution.TrainerIndexPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('surname'),
        FieldPanel('name'),
        FieldPanel('name2'),
        FieldPanel('foto'),
        FieldPanel('birth'),
        FieldPanel('education'),
        FieldPanel('ranks'),
    ]


class TrainerIndexPage(Page):
    body = RichTextField(blank=True)
    
    def get_context(self, request):
        context = super().get_context(request)
        pages = self.get_children().live().order_by('trainerpage__name')
        context['trainerpages'] = pages
        return context
    
    subpage_types = ['institution.TrainerPage']
    parent_page_types = ['institution.InstitutionPage']
    
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
