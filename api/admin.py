from django.contrib import admin

from api import constants as _
from api.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class GenreTitleInLine(admin.TabularInline):
    model = GenreTitle
    extra = 1


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    empty_value_display = _.EMPTY_VALUE_MESSAGE


@admin.register(Genre)
class Genre(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    inlines = (GenreTitleInLine,)
    empty_value_display = _.EMPTY_VALUE_MESSAGE


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'year',
        'description',
        'get_genres',
    )
    inlines = (GenreTitleInLine,)
    list_filter = (
        'category',
        'genre',
        'year',
        'description',
    )
    search_fields = (
        'name',
    )
    empty_value_display = _.EMPTY_VALUE_MESSAGE

    def get_genres(self, obj):
        genres = obj.genre.values_list('name', flat=True)
        return ', '.join(genres)

    get_genres.short_description = 'Жанр'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'text',
        'pub_date',
    )
    list_filter = (
        'title',
        'author',
        'pub_date',
    )
    search_fields = (
        'text',
    )
    empty_value_display = _.EMPTY_VALUE_MESSAGE


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'pub_date',
        'review',
    )
    list_filter = (
        'author',
        'pub_date',
        'review',
    )
    search_fields = (
        'text',
    )
    empty_value_display = _.EMPTY_VALUE_MESSAGE


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    list_filter = (
        'role',
    )
    search_fields = (
        'bio',
    )
    empty_value_display = _.EMPTY_VALUE_MESSAGE
