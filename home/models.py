from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from event.models import EventPage
from datetime import date, timedelta, datetime
from wagtailvideos.edit_handlers import VideoChooserPanel
from modelcluster.fields import ParentalKey
import pytz



class HomePage(Page):
    """
    Домашняя страница: 
        - раздел hero с фоновым видео, слоганом (текст) и двумя (или одной) кнопками;
        - слайдер с блоком произвольного RichText содержимого в каждом слайде;
        - строка дней календаря для отображения событий (EventPage) за период (JavaCript & Fetch JsonAPI)
    """    
    video = models.ForeignKey('wagtailvideos.Video', related_name='+', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Видео секции HERO")
    slogan = models.CharField(blank=True, max_length=255, verbose_name="Слоган на видео", help_text='Текст на фоне видео')
    timer_date = models.DateTimeField('Дата и время наступления события', blank=True, null=True)
    button_register = models.CharField(blank=True, verbose_name="Кнопка регистрации", max_length=16, help_text="Регистрация")
    link_register = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name='Hero ссылка для регистрации', help_text='Выбрать страницу, для перехода по кнопке')
    button_info = models.CharField(blank=True, verbose_name="Кнопка информации", max_length=16, help_text="Подробнее")
    link_info = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name='Hero ссылка "Подробнее"', help_text='Выбрать страницу, для перехода по кнопке')
    body = RichTextField(blank=True)
    
    max_count = 1   # Всего одна домашняя страница, всего один сайт

    def get_context(self, request):
        context = super().get_context(request)
        date_ = date.today() # начало календаря с сегодняшней даты
        days = [] # дни месяца
        months = [] # месяцы
        month_ = '' # месяц, дни которого заполняем
        str_weekdays = [ "пн", "вт", "ср", "чт", "пт", "сб", "вс",]
        str_months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
        i = 40 # столько дней календаря событий будем выводить
        month_ = str_months[date_.month - 1] # начнем с текущего
        while i:
            if (str_months[date_.month - 1] != month_): # если не текущий месяц, то начинаем новый
                months += [
                    [month_, {'days': days}],    # сохраняем дни этого месяца
                ]
                days = [] # обнуляем
            month_ = str_months[date_.month - 1] # начинаем новый месяц
            days += [   # прибавим день в текущий месяц
                [date_.__str__(), date_.day, str_weekdays[date_.weekday()]]
                ]
            date_ += timedelta(days=1) 
            i -= 1
        months += [ # по завершении цикла сохраним данные последнего набора
            [month_, {'days': days}],    # сохраняем дни этого месяца
        ]
        context['calendar'] = months
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("slogan"),
                FieldPanel('timer_date'),
                VideoChooserPanel('video'),
                FieldPanel("button_register"),
                FieldPanel("link_register"),
                FieldPanel("button_info"),
                FieldPanel("link_info"),
            ], heading="Раздел Hero"
        ),
        InlinePanel('slider', heading='Слайдер', label="Слайд"),
        FieldPanel('body', heading='Произвольное содержимое', help_text="Не желательно, только если очень важно"),
    ]

    class Meta:
        verbose_name= 'Домашняя страница'



class Slider(Orderable):
    """ Страницы слайдера, внутри RichText блок произвольного содержимого """
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='slider')
    content = RichTextField(blank=False, verbose_name='Содержимое')
    
    panels = [
        FieldPanel('content'),
    ]
