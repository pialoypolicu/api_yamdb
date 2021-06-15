# Generated by Django 3.0.5 on 2021-06-15 11:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210615_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(default=10, help_text='Введите от 0 до 10', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка'),
        ),
    ]
