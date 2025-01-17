# Generated by Django 5.1.5 on 2025-01-17 07:20

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
        ('wagtailimages', '0027_image_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Учреждения',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='TrainerIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Тренеры',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='InstitutionPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('name', models.CharField(max_length=512, verbose_name='Наименование')),
                ('description', wagtail.fields.RichTextField(blank=True, verbose_name='Описание')),
                ('site', models.CharField(blank=True, max_length=512, verbose_name='Сайт')),
                ('logo', models.ForeignKey(blank=True, help_text='Логотип', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Учреждение',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='TrainerPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('surname', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('name2', models.CharField(blank=True, max_length=64, null=True, verbose_name='Отчество')),
                ('birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('education', models.CharField(blank=True, max_length=128, null=True, verbose_name='Образование')),
                ('ranks', models.CharField(blank=True, max_length=128, null=True, verbose_name='Звания и достижения')),
                ('foto', models.ForeignKey(blank=True, help_text='Фотография', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Фото')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trainer', to='institution.institutionpage', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Тренер',
            },
            bases=('wagtailcore.page',),
        ),
    ]
