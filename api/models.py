from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Categories(models.Model):
    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=200,
        help_text='Введите категорию'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
