from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel, FieldRowPanel, InlinePanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import  DraftStateMixin, PreviewableMixin, RevisionMixin, TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from modelcluster.fields import ParentalKey



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
    

class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name='form_fields')
    
    
    
class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Поля формы"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address'),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),
        ], 'Email'),
    ]
