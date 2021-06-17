# Generated by Django 3.0.5 on 2021-06-17 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
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
    ]