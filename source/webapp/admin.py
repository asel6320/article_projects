from django.contrib import admin

from webapp.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_display_links = ['id', 'title']
    list_filter = ['author']
    search_fields = ['title', 'content']
    fields = ['title', 'author', 'content', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
# Register your models here.
admin.site.register(Article, ArticleAdmin)