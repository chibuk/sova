from django.contrib import admin

# from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
# from institution.models import LocationPage

# class SportModelAdmin(ModelAdmin):
#     model = LocationPage
#     menu_label = 'Объект спорта'
#     menu_icon = 'placeholder'  # Название и иконка
#     add_to_settings_menu = False
#     exclude_from_main_menu = False

#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         # Фильтрация объектов, которые будут отображаться в ManyToManyField
#         if db_field.name == 'locations':
#             kwargs['queryset'] = LocationPage.objects.filter(is_published=True)  # пример фильтрации
#         return super().formfield_for_manytomany(db_field, request, **kwargs)

# # Регистрация админки
# modeladmin_register(SportModelAdmin)
