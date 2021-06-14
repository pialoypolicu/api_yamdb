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


class Titles(models.Model):
    title = models.CharField('Name', max_length=200, help_text='Введи название')
    # category = models.ForeignKey(Catigories, on_delete=models.CASCADE, related_name='категория')
    year = models.SmallIntegerField('Year', help_text='Год выхода', null=True)

    class Meta:
        verbose_name_plural = 'Titles'
