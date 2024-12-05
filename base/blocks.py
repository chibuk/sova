from wagtail.blocks import (
    ChooserBlock,
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock



class CaptionedImageBlock(StructBlock):
    image = ImageBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)
    
    class Meta: 
        icon = 'image'
        template = "base/blocks/captioned_image_block.html"
        
        
class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Выбрать размер заголовка"),
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
        ],
        blank=True,
        required=False,
    )
    
    class Meta: 
        icon = 'title'
        template = 'base/blocks/heading_block.html'
        
        
class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = CaptionedImageBlock()
    embded_block = EmbedBlock(
        help_text="Ввести URL для встраивания, например, https://rutube.ru/video/da422a2520db8cc2705357e858aaba98/",
        icon="media",
    )
        
