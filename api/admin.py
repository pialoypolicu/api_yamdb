from django.contrib import admin

from api.models import Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year')


admin.site.register(Title, TitleAdmin)
