from django.contrib import admin
from .models import Transaction, Batch, WalletProfile

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("tx_hash", "from_address", "to_address", "amount", "timestamp", "is_anomaly", "risk_label")
    search_fields = ("tx_hash", "from_address", "to_address")
    list_filter = ("is_anomaly", "risk_label")

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("batch_name", "created")  # actual fields from your model
    list_filter = ("batch_name",)

@admin.register(WalletProfile)
class WalletProfileAdmin(admin.ModelAdmin):
    list_display = ("wallet_id", "balance")  # actual fields from your model
    list_filter = ("balance",)
    ordering = ("wallet_id",)

