from django.contrib import admin

from api.models import Title, User

admin.site.register(Title)


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
