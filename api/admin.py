from django.contrib import admin

from api.models import Review, Title
from users.models import User


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'pub_date')


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)


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
    empty_value_display = '-пусто-'
