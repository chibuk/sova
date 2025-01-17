from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from portfolio.blocks import PortfolioStreamBlock


class PortfolioPage(Page):
    body = StreamField(
        PortfolioStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Используйте '+' чтобы выбрать тип блока и добавить содержимое",
    )

    description = 'Страница PortfolioPage, с произвольным содержимым и фрагментами из блога'

    content_panels = Page.content_panels + [
        FieldPanel("body", heading='Блок содержимого'),
    ]

    parent_page_types = ['home.HomePage', "institution.InstitutionPage"]
    subpage_types = ['portfolio.PortfolioPage', 'base.FormPage']
    
    class Meta:
        verbose_name = 'Внутренняя страница'
