from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting

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
