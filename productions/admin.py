from django.contrib import admin
from .models import Article, EventWork, PublishedBook, PublishedChapter


# Admin models for CommonFields model
class CommonFieldsAdmin(admin.ModelAdmin):
    list_display = ("title", "researcher", "year", "language")
    search_fields = ("title", "researcher__name")


# Admin models for Article model
class ArticleAdmin(CommonFieldsAdmin):
    list_display = CommonFieldsAdmin.list_display + (
        "periodical_title",
        "publication_location",
    )
    search_fields = CommonFieldsAdmin.search_fields + (
        "periodical_title",
        "publication_location",
    )


# Admin models for EventWork model
class EventWorkAdmin(CommonFieldsAdmin):
    list_display = CommonFieldsAdmin.list_display + (
        "event_name",
        "event_city",
        "publisher_name",
    )
    search_fields = CommonFieldsAdmin.search_fields + (
        "event_name",
        "event_city",
        "publisher_name",
    )


# Admin models for PublishedBook model
class PublishedBookAdmin(CommonFieldsAdmin):
    list_display = CommonFieldsAdmin.list_display + ("volume", "publisher")
    search_fields = CommonFieldsAdmin.search_fields + ("volume", "publisher")


# Admin models for PublishedChapter model
class PublishedChapterAdmin(CommonFieldsAdmin):
    list_display = CommonFieldsAdmin.list_display + (
        "book_title",
        "organizers",
        "publisher",
    )
    search_fields = CommonFieldsAdmin.search_fields + (
        "book_title",
        "organizers",
        "publisher",
    )


# Register the models with the admin site
admin.site.register(Article, ArticleAdmin)
admin.site.register(EventWork, EventWorkAdmin)
admin.site.register(PublishedBook, PublishedBookAdmin)
admin.site.register(PublishedChapter, PublishedChapterAdmin)
