from django.contrib import admin

from api.models import Title, User, Review

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
        'description',
        'first_name',
        'last_name',
    )
    list_filter = (
        'role',
    )
    search_fields = (
        'description',
    )
    empty_value_display = '-пусто-'
