from django.contrib import admin
from .models import DashboardExample

@admin.register(DashboardExample)
class DashboardExampleAdmin(admin.ModelAdmin):
    list_display = ("title",)  # only include fields that actually exist
    search_fields = ("name",)           # only searchable fields that exist
    list_filter = ()                     # only fields that exist
    ordering = ("id",)                  # only fields that exist

