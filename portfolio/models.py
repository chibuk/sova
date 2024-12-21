from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from portfolio.blocks import PortfolioStreamBlock


class PortfolioPage(Page):
    parent_page_types = ["home.HomePage"]

    body = StreamField(
        PortfolioStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Используйте '+' чтобы выбрать тип блока и добавить содержимое",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body", heading='Блок содержимого'),
    ]
    