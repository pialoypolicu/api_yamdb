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
    name = models.CharField('Name', max_length=200, help_text='Введи название')
    year = models.PositiveSmallIntegerField('Year', help_text='Год выхода', null=True)
    description = models.TextField('Описание', null=True)
    # category = models.ForeignKey(Catigories, related_name='title')
    genre = models.CharField('Жанр', max_length=50, null=True)
    category = models.IntegerField('Категория', null=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

class Review(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='review')
    text = models.TextField('Текст отзыва', help_text='Введите текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # score = models.PositiveSmallIntegerField('Оценка', help_text='Введите от 0 до 10', default=10)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
