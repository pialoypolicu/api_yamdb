from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.utils import wrap_text
from api.validators import validate_year
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        help_text='Введите категорию', db_index=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        help_text='Введите жанр'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        help_text='Введите название',
    )
    year = models.PositiveSmallIntegerField(
        'Год',
        help_text='Год выхода',
        null=True,
        db_index=True,
        validators=(validate_year,)
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)

    def __str__(self):
        description = None
        if self.description:
            description = wrap_text(self.description)
        genre = None
        if self.genre:
            genre = ''.join([title.name for title in self.genre.all()])
        return (
            f'id: {self.id}\n'
            f'Name: {self.name}\n'
            f'Year: {self.year}\n'
            f'Description: {description}\n'
            f'Category: {self.category}\n'
            f'Genre: {genre}\n'
            f'\n'
        )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        db_index=True,
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        help_text='Введите от 1 до 10',
        default=10,
        validators=[
            MinValueValidator(1, message='Оценка не может быть ниже 1.'),
            MaxValueValidator(10, message='Оценка не может быть больше 10.')
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        text = wrap_text(self.text)
        return (
            f'id: {self.id}\n'
            f'Author: {self.author.username}\n'
            f'Date: {self.pub_date}\n'
            f'Title: {self.title.name}\n'
            f'Score: {self.score}\n'
            f'Text: {text}\n'
            f'\n'
        )


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комметария',
        help_text='Введите текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        text = wrap_text(self.text)
        return (
            f'id: {self.id}\n'
            f'Author: {self.author.username}\n'
            f'Date: {self.pub_date}\n'
            f'Review: {self.review_id}\n'
            f'Text: {text}\n'
            f'\n'
        )
