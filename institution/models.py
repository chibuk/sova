'''Учреждения -> Объекты, Тренеры, Виды спорта, Услуги'''
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
    subpage_types = [
        'institution.TrainerIndexPage',
        'institution.LocationIndexPage',
        'institution.SportIndexPage',
    ]
    parent_page_types = ['institution.InstitutionIndexPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('description'),
        FieldPanel('site'),
    ]

    class Meta:
        verbose_name = "Учреждение"



class InstitutionIndexPage(Page):
    body = RichTextField(blank=True)
    
    parent_page_types = ['home.HomePage']
    subpage_types = ['institution.InstitutionPage']
    
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Индекс Учреждений"



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



class TrainerPage(Page, InstitutionMixin):
    surname = models.CharField('Фамилия', max_length=64)
    name = models.CharField('Имя', max_length=64)
    name2 = models.CharField('Отчество', max_length=64, null=True, blank=True)
    photo = models.ForeignKey('wagtailimages.Image', null=True, blank=True, verbose_name="Фото",
                                   on_delete=models.SET_NULL, related_name='+', help_text='Фотография')
    birth = models.DateField('Дата рождения', blank=True, null=True)
    education = models.CharField('Образование', max_length=128, null=True, blank=True)
    ranks = models.CharField('Звания и достижения', max_length=128, null=True, blank=True)

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
        FieldPanel('photo'),
        FieldPanel('birth'),
        FieldPanel('education'),
        FieldPanel('ranks'),
        InlinePanel('category', label="Категория"),
    ]

    class Meta:
        verbose_name = "Тренер"



class TrainerCategory(Orderable):
    page = ParentalKey(TrainerPage, on_delete=models.CASCADE, related_name='category')
    name = models.CharField('Категория', max_length=256, choices=[
        ('Тренер высшей квалификационной категории', 'Тренер высшей квалификационной категории'),
        ('Тренер первой квалификационной категории', 'Тренер первой квалификационной категории'),
        ('Тренер второй квалификационной категории', 'Тренер второй квалификационной категории'),
    ])
    end_date = models.DateField("Срок до", blank=True, help_text="Введите дату")

    panels = [
        FieldPanel('name'),
        FieldPanel('end_date'),
    ]



class TrainerIndexPage(Page):
    body = RichTextField(blank=True)
    
    subpage_types = ['institution.TrainerPage']
    parent_page_types = ['institution.InstitutionPage']
    
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Индекс Тренеров"



class LocationPage(Page, InstitutionMixin):
    """Объекты, базы, катки, арены.
    Поля: фото объекта, фотографии залов, адрес, описание, контакты, режим работы"""
    name = models.CharField('Наименование', max_length=128)
    photo = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='+', verbose_name="Главное фото объекта")
    address = models.CharField(max_length=255, verbose_name="Адрес", null=True, blank=True)
    body = RichTextField(blank=True)
    contacts = models.CharField(max_length=255, verbose_name="Контакты", null=True, blank=True)
    opening_hours = models.CharField(max_length=255, verbose_name="Режим работы", null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('address'),
        index.SearchField('body'),
    ]

    subpage_types = []
    parent_page_types = ['institution.LocationIndexPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('photo'),
        FieldPanel('address'),
        FieldPanel('body'),
        FieldPanel('contacts'),
        FieldPanel('opening_hours'),
        InlinePanel('photos', label="Фтографии залов, арен, катков"),
    ]

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"



class LocationPhotos(Orderable):
    """Фотографии залов объекта"""
    page = ParentalKey(LocationPage, on_delete=models.CASCADE, related_name='photos')
    photo = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+', verbose_name="Фотография")
    description = models.CharField('Описание', max_length=256, null=True, blank=True)

    panels = [
        FieldPanel('photo'),
        FieldPanel('description'),
    ]



class LocationIndexPage(Page):
    body = RichTextField(blank=True)
    
    subpage_types = ['institution.LocationPage']
    parent_page_types = ['institution.InstitutionPage']
    
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
        
    class Meta:
        verbose_name = "Индекс Объектов (Здания, Базы и т.п.)"



class SportPage(Page, InstitutionMixin):
    ''' Виды спорта, наименование, тренеры, объекты '''
    name = models.CharField('Наименование', max_length=128)
    logo = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="Логотип 60х60")
    trainers = models.ManyToManyField(TrainerPage, blank=True, verbose_name="Тренеры", related_name='sports')
    locations = models.ManyToManyField(LocationPage, blank=True, verbose_name="Объекты", related_name='sports')
    
    subpage_types = []
    parent_page_types = ['institution.SportIndexPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('trainers'),
        FieldPanel('locations'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
    
    class Meta:
        verbose_name = 'Вид спорта'



class SportIndexPage(Page):
    body = RichTextField(blank=True)
    
    subpage_types = ['institution.SportPage']
    parent_page_types = ['institution.InstitutionPage']
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    class Meta:
        verbose_name = "Индекс Видов спорта"
