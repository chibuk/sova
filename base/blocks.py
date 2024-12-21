from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock



class CaptionedImageBlock(StructBlock):
    image = ImageBlock(required=True, label="Изображение")
    caption = CharBlock(required=False, label="Название")
    attribution = CharBlock(required=False, help_text='Будет через тире после названия', label="Расшифровка")
    
    class Meta: 
        icon = 'image'
        template = "base/blocks/captioned_image_block.html"
        label="Изображение с подписью"
        
        
class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True, label="Текст заголовка")
    size = ChoiceBlock(
        choices=[
            ("", "Выбрать размер заголовка"),
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
        ],
        blank=True, label="Уровень", required=False,
    )
    
    class Meta: 
        icon = 'title'
        template = 'base/blocks/heading_block.html'
        label="Заголовок"
        
        
class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow", label="Параграф")
    image_block = CaptionedImageBlock(label="Изображение")
    embded_block = EmbedBlock(
        help_text="Ввести URL для встраивания, например, https://rutube.ru/video/da422a2520db8cc2705357e858aaba98/",
        icon="media", label="Встроенный блок",
    )
        
