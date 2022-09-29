from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'category', 'created_at', 'update_at', 'is_published',
        'get_photo')  # Что будет отображатся в админке
    list_display_links = ('id', 'title')  # Передать, то будет ссылками на записи
    search_fields = ('title', 'content')  # Добавление поиска по указанным полям
    list_editable = ('is_published',)  # Добавить возможность редактировать на месте
    list_filter = ('is_published', 'category')  # Добавить фильтр поиска
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'views', 'created_at', 'update_at')
    readonly_fields = ('get_photo', 'views', 'created_at', 'update_at')
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}", width="75"')
        else:
            return 'фото не загружено'

    get_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')  # Что будет отображатся в админке
    list_display_links = ('id', 'title')  # Передать, то будет ссылками на записи
    search_fields = ('title',)  # Добавление поиска по указанным полям


admin.site.register(News, NewsAdmin)  # Порядок важен
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
