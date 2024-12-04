from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import  DraftStateMixin, PreviewableMixin, RevisionMixin, TranslatableMixin
from wagtail.snippets.models import register_snippet



@register_setting
class NavigationSettings(BaseGenericSetting):
    vk_url = models.URLField(verbose_name="Ссылка VK", blank=True)
    github_url = models.URLField("Ссылка на GitHub", blank=True)
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('vk_url'),
                FieldPanel('github_url'),
            ], "Настройки соцсетей",
        )
    ]

@register_snippet
class FooterText(
    DraftStateMixin, 
    RevisionMixin, 
    PreviewableMixin, 
    TranslatableMixin,
    models.Model,
    ):
        
    '''
    Текстовые блоки (body: RichText) футера.
    '''
        
    body = RichTextField()
    
    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]
    
    def __str__(self):
        return "Текст footer'а"
    
    def get_preview_template(self, request, mode_name):
        return "base.html"
    
    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}
    
    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Тексты футера"
    
