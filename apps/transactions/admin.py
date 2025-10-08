from django.contrib import admin
from .models import Transaction, Batch, WalletProfile

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("tx_hash", "from_address", "to_address", "amount", "timestamp", "is_anomaly", "risk_label")
    search_fields = ("tx_hash", "from_address", "to_address")
    list_filter = ("is_anomaly", "risk_label")
    ordering = ("-timestamp",)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")  # remove 'status' if it doesn't exist
    search_fields = ("id",)
    list_filter = ("created_at",)         # remove 'status' if it doesn't exist
    ordering = ("-created_at",)

@admin.register(WalletProfile)
class WalletProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")    # remove 'created_at' if not in model
    list_filter = ()                      # only use fields that exist
    ordering = ("user",)


