from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Titles(models.Model):
    title = models.CharField('Name', max_length=200, help_text='Введи название')
    # category = models.ForeignKey(Catigories, on_delete=models.CASCADE, related_name='категория')
    year = models.SmallIntegerField('Year', help_text='Год выхода', null=True)


    class Meta:
        verbose_name_plural = 'Titles'
