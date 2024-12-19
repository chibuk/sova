from base.blocks import BaseStreamBlock
from wagtail.blocks import (
    CharBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StructBlock,
)
from wagtail.images.blocks import ImageBlock
from base.blocks import BaseStreamBlock


class CardBlock(StructBlock):
    heading = CharBlock(label='Заголовок')
    text = RichTextBlock(features=['bold', 'italic', 'link'], label='Содержание')
    image = ImageBlock(required=False, label='Изображение')
    
    class Meta:
        icon = "form"
        template = "portfolio/blocks/card_block.html"
        label='Карточка'
        
        
class FeaturePostsBlock(StructBlock):
    heading = CharBlock(label='Заголовок')
    text = RichTextBlock(features=["bold", "italic", "link"], required=False, label='Содержание')
    posts = ListBlock(PageChooserBlock(page_type="blog.BlogPage"), label='Записи блога')
    
    class Meta:
        icon = "folder-open-inverse"
        template = "portfolio/blocks/featured_posts_block.html"
        label='Записи из блога'


class PortfolioStreamBlock(BaseStreamBlock):
    card = CardBlock(group="Блоки портфолио")
    featured_posts = FeaturePostsBlock(group="Блоки портфолио")

    class Meta:
        label='Содержание'
