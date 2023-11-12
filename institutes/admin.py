from django.contrib import admin
from .models import Institute


class InstituteAdmin(admin.ModelAdmin):
    list_display = ["acronym", "institute_code", "country_acronym", "country"]
    search_fields = ["acronym", "institute_code", "country_acronym", "country"]


admin.site.register(Institute, InstituteAdmin)
