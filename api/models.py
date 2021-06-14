from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    name = models.CharField('Name', max_length=200, help_text='Введи название')
    # category = models.ForeignKey(Catigories, related_name='title')
    category = models.IntegerField('Категория', )
    year = models.SmallIntegerField('Year', help_text='Год выхода', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'
