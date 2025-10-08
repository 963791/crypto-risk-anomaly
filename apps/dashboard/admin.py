from django.contrib import admin
from .models import DashboardExample

@admin.register(DashboardExample)
class DashboardExampleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # only fields in model
    list_filter = ('name',)  # optional
    ordering = ('name',)

