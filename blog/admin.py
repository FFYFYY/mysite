from django.contrib import admin
from .models import Blogtype, Blog


@admin.register(Blogtype)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'discription')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_filter = ['blogtype']
    list_display = ('title', 'blogtype', 'created_time',)
