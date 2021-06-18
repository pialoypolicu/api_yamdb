from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=200,
        help_text='Введите категорию'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Наименование жанра',
        max_length=200,
        help_text='Введите жанр'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Name', max_length=200, help_text='Введи название')
    year = models.PositiveSmallIntegerField(
        'Year',
        help_text='Год выхода',
        null=True
    )
    description = models.TextField('Описание', null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('Текст отзыва', help_text='Введите текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        'Оценка',
        help_text='Введите от 1 до 10',
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    comment = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('Текс комметария', help_text='Введите текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
