# Generated by Django 3.0.5 on 2021-06-17 14:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите категорию', max_length=200, verbose_name='Наименование категории')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст', verbose_name='Текст отзыва')),
                ('score', models.PositiveSmallIntegerField(default=10, help_text='Введите от 1 до 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введи название', max_length=200, verbose_name='Name')),
                ('year', models.PositiveSmallIntegerField(help_text='Год выхода', null=True, verbose_name='Year')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('genre', models.CharField(max_length=50, null=True, verbose_name='Жанр')),
                ('category', models.IntegerField(null=True, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Название',
                'verbose_name_plural': 'Названия',
            },
        ),
    ]
