from django.db import models
from django import forms

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase



class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['blog.BlogPage', 'blog.BlogTagIndexPage']
    parent_page_types = ['home.HomePage']

    class Meta:
        verbose_name = "Блог, индексная страница"


class BlogTagPage(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tegged_items', on_delete=models.CASCADE)


class BlogPage(Page):
    date = models.DateField("Дата публикации")
    intro = models.CharField('Заголовок', max_length=250)
    body = RichTextField('Текст', blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogTagPage, blank=True)

    subpage_types = []
    parent_page_types = ['blog.BlogIndexPage']

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else: 
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
           FieldPanel('date'),
           FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
           FieldPanel('tags'), 
        ], heading='Информация о блоге'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label='Галерея изображений'),
    ]

    class Meta:
        verbose_name = "Запись блога"


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField('Заголовок', blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Авторы"


class BlogTagIndexPage(Page):

    subpage_types = []
    parent_page_types = ['blog.BlogIndexPage']
    
    def get_context(self, requesst):
        tag = requesst.GET.get('tag')
        blogpages = BlogPage.objects.live().filter(tags__name=tag)
        context = super().get_context(requesst)
        context['blogpages'] = blogpages
        return context

    class Meta:
        verbose_name = "Индексная страница тегов блога"
