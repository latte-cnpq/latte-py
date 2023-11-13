# admin.py

from django.contrib import admin
from .models import Production, Article, PublishedBook, PublishedChapter


# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ("title", "researcher", "year", "periodical_title")
#     search_fields = ("title", "researcher__name")


# @admin.register(PublishedBook)
# class PublishedBookAdmin(admin.ModelAdmin):
#     list_display = ("title", "researcher", "year", "publisher")
#     search_fields = ("title", "researcher__name")


# @admin.register(PublishedChapter)
# class PublishedChapterAdmin(admin.ModelAdmin):
#     list_display = ("title", "researcher", "year", "book_title")
#     search_fields = ("title", "researcher__name")


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ("title", "researcher", "year", "type")
    search_fields = ("title", "researcher__name")
