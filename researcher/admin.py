from django.contrib import admin
from .models import Researcher


class ResearcherAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "researcher_id"]
    search_fields = ["name", "email", "researcher_id"]
    list_filter = ["institutes"]


admin.site.register(Researcher, ResearcherAdmin)
