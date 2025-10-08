from django.contrib import admin
from .models import Transaction, Batch, WalletProfile

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("tx_hash", "from_address", "to_address", "amount", "timestamp", "is_anomaly", "risk_label")
    search_fields = ("tx_hash", "from_address", "to_address")
    list_filter = ("is_anomaly", "risk_label", "timestamp")
    ordering = ("-timestamp",)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "status")
    search_fields = ("id",)
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)

@admin.register(WalletProfile)
class WalletProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance", "created_at")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

