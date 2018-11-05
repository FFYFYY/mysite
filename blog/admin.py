from django.contrib import admin
from .models import Blogtype, Blog


@admin.register(Blogtype)
class BlogtypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'discription')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    date_hierarchy = 'created_time'
    list_filter = ['blogtype']
    list_display = ('title', 'blogtype', 'created_time',)
