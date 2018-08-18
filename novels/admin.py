from django.contrib import admin
from .models import Booktype, Novel, Chapter

@admin.register(Booktype)
class BooktypeAdmin(admin.ModelAdmin):
    list_display = ('booktype',)


@admin.register(Novel)
class NovelsAdmin(admin.ModelAdmin):
    list_display = ('bookname', 'author', 'booktype', 'read_count', 'search_count')
    fields = ('bookname', 'author', 'summary', 'booktype')

@admin.register(Chapter)
class NovelAdmin(admin.ModelAdmin):
    list_display = ('chapter_title', 'chapter_num', 'bookname')

