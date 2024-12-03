from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):
    
    image = models.ForeignKey(
        'wagtailimages.Image', 
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Изображение домашней страницы',
    )
    hero_text = models.CharField(blank=True, max_length=255, help_text='Напиши краткое введение')
    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Текст выводимый на CTA",
    )
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name='Hero CTA ссылка',
        help_text='Выбрать страницу, с призывом к действию (CTA)'
    )    
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                FieldPanel("hero_cta"),
                FieldPanel("hero_cta_link"),
            ], heading="Раздел Hero"
        ),
        FieldPanel('body'),
    ]
