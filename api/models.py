from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    description = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=100,
        choices=Roles.choices,
        default=Roles.USER,
    )


class Title(models.Model):
    title = models.CharField('Name', max_length=200, help_text='Введи название')
    # category = models.ForeignKey(Catigories, related_name='title')
    category = models.IntegerField('Категория', )
    year = models.SmallIntegerField('Year', help_text='Год выхода', null=True)
