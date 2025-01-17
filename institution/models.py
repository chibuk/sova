'''Учреждения'''
from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from modelcluster.fields import ParentalKey


class InstitutionPage(Page):
    '''Учреждение, в данной модели есть Тренеры, Объекты и другие дочерние модели
    их индексные страницы являются непосрественными потомками этой модели
    Наслдеование древовидное'''

    name = models.CharField('Наименование', max_length=512)
    logo = models.ForeignKey('wagtailimages.Image', null=True, blank=True, verbose_name="Логотип",
                                   on_delete=models.SET_NULL, related_name='+', help_text='Логотип')
    description = RichTextField('Описание', blank=True)
    site = models.CharField('Сайт', max_length=512, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('description'),
    ]
    subpage_types = ['institution.TrainerIndexPage']
    parent_page_types = ['institution.InstitutionIndexPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('description'),
        FieldPanel('site'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        pages = self.get_children().live() #.not_type(TrainerPage) # в not_type добавляем всех неиндексных детей
        context['indexpages'] = pages
        return context

    class Meta:
        verbose_name = "Учреждение"


class InstitutionIndexPage(Page):
    
    body = RichTextField(blank=True)
    
    def get_context(self, request):
        context = super().get_context(request)
        pages = self.get_children().live().order_by('institutionpage__name')
        context['institutionpages'] = pages
        return context
    
    parent_page_types = ['home.HomePage']
    subpage_types = ['institution.InstitutionPage']
    
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Учреждения"


class TrainerPage(Page):
    surname = models.CharField('Фамилия', max_length=64)
    name = models.CharField('Имя', max_length=64)
    name2 = models.CharField('Отчество', max_length=64, null=True, blank=True)
    foto = models.ForeignKey('wagtailimages.Image', null=True, blank=True, verbose_name="Фото",
                                   on_delete=models.SET_NULL, related_name='+', help_text='Фотография')
    birth = models.DateField('Дата рождения', blank=True, null=True)
    education = models.CharField('Образование', max_length=128, null=True, blank=True)
    ranks = models.CharField('Звания и достижения', max_length=128, null=True, blank=True)
    
    institution = models.ForeignKey(
        InstitutionPage,
        on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='trainer', 
        verbose_name='Организация') # default=)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('surname'),
    ]
    subpage_types = []
    parent_page_types = ['institution.TrainerIndexPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('surname'),
        FieldPanel('name'),
        FieldPanel('name2'),
        FieldPanel('foto'),
        FieldPanel('birth'),
        FieldPanel('education'),
        FieldPanel('ranks'),
        InlinePanel('category', label="Категория"),
    ]

    def save(self, *args, **kwargs):
        # Здесь указываем логику для нахождения "деда"
        self.institution = self.get_institution() #institution_page
        super().save(*args, **kwargs)

    def get_institution(self):
        return InstitutionPage.objects.ancestor_of(self, inclusive=False).last()

    class Meta:
        verbose_name = "Тренер"


class TrainerCategory(Orderable):
    page = ParentalKey(TrainerPage, on_delete=models.CASCADE, related_name='category')
    category = models.CharField('Категория', max_length=256, choices=[
        ('Тренер высшей квалификационной категории', 'Тренер высшей квалификационной категории'),
        ('Тренер первой квалификационной категории', 'Тренер первой квалификационной категории'),
        ('Тренер второй квалификационной категории', 'Тренер второй квалификационной категории'),
    ])
    end_date = models.DateField("Срок до", blank=True, help_text="Введите дату")

    panels = [
        FieldPanel('category'),
        FieldPanel('end_date'),
    ]


class TrainerIndexPage(Page):
    body = RichTextField(blank=True)
    
    def get_context(self, request):
        context = super().get_context(request)
        pages = TrainerPage.objects.live().filter(institution=self.get_parent()).order_by('name')
        context['trainerpages'] = pages
        return context
    
    subpage_types = ['institution.TrainerPage']
    parent_page_types = ['institution.InstitutionPage']
    
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Тренеры"



class InstitutionMixin(models.Model):
    """Добавит связанное с 'дедушкой' поле institution и механизм его авто(заполнения)сохранения
    Важно: по умолчанию related_name=classname_set т.к. у нас ForeignKey отношение"""
    institution = models.ForeignKey(InstitutionPage, on_delete=models.SET_NULL, 
        null=True, blank=True, verbose_name='Уреждение')

    def save(self, *args, **kwargs):
        # Здесь указываем логику для нахождения "деда"
        self.institution = self.get_institution() #institution_page
        super().save(*args, **kwargs)

    def get_institution(self):
        return InstitutionPage.objects.ancestor_of(self, inclusive=False).last()

    class Meta:
        abstract = True



class LocationPage(Page, InstitutionMixin):
    """Объекты, здания, катки, арены.
    Поля: фото объекта и залов, адрес, описание, контакты, режим работы"""
    # surname = models.CharField('Фамилия', max_length=64)
    # name = models.CharField('Имя', max_length=64)
    # name2 = models.CharField('Отчество', max_length=64, null=True, blank=True)
    # foto = models.ForeignKey('wagtailimages.Image', null=True, blank=True, verbose_name="Фото",
    #                                on_delete=models.SET_NULL, related_name='+', help_text='Фотография')
    # birth = models.DateField('Дата рождения', blank=True, null=True)
    # education = models.CharField('Образование', max_length=128, null=True, blank=True)
    # ranks = models.CharField('Звания и достижения', max_length=128, null=True, blank=True)

    # search_fields = Page.search_fields + [
    #     index.SearchField('name'),
    #     index.SearchField('surname'),
    # ]

    # subpage_types = []
    # parent_page_types = ['institution.TrainerIndexPage']
    
    # content_panels = Page.content_panels + [
    #     FieldPanel('surname'),
    #     FieldPanel('name'),
    #     FieldPanel('name2'),
    #     FieldPanel('foto'),
    #     FieldPanel('birth'),
    #     FieldPanel('education'),
    #     FieldPanel('ranks'),
    #     InlinePanel('category', label="Категория"),
    # ]

    class Meta:
        verbose_name = "Объект"


class ДщсфешщтIndexPage(Page):
    # body = RichTextField(blank=True)
    
    # def get_context(self, request):
    #     context = super().get_context(request)
    #     pages = TrainerPage.objects.live().filter(institution=self.get_parent()).order_by('name')
    #     context['trainerpages'] = pages
    #     return context
    
    # subpage_types = ['institution.TrainerPage']
    # parent_page_types = ['institution.InstitutionPage']
    
    # content_panels = Page.content_panels + [
    #     FieldPanel("body"),
    # ]

    class Meta:
        verbose_name = "Объекты"
