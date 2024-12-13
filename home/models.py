from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from wagtailvideos.edit_handlers import VideoChooserPanel


class HomePage(Page):
    
    # image = models.ForeignKey(
    #     'wagtailimages.Image', 
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+',
    #     help_text='Изображение домашней страницы',
    # )
    hero_video = models.ForeignKey('wagtailvideos.Video',
                                   related_name='+', null=True, on_delete=models.SET_NULL)
    hero_text = models.CharField(blank=True, max_length=255, help_text='Слоган на фоне видео')
    hero_button = models.CharField(blank=True, verbose_name="Текст кнопки", max_length=16,
        help_text="Текст кнопки",
    )
    hero_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name='Hero ссылка',
        help_text='Выбрать страницу, для перехода по кнопке на фоне видео'
    )    
    body = RichTextField(blank=True)
    
    # parent_page_types = ['root']

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                # FieldPanel("image"),
                FieldPanel("hero_text"),
                VideoChooserPanel('hero_video'),
                FieldPanel("hero_button"),
                FieldPanel("hero_link"),
            ], heading="Раздел Hero"
        ),
        FieldPanel('body'),
    ]
