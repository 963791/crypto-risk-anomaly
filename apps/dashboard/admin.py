from django.contrib import admin
from .models import DashboardExample

@admin.register(DashboardExample)
class DashboardExampleAdmin(admin.ModelAdmin):
    list_display = ("title",)  # only include fields that actually exist
