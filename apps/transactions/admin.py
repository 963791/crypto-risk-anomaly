from django.contrib import admin
from .models import Transaction, Batch, WalletProfile

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("tx_hash","from_address","to_address","amount","timestamp","is_anomaly","risk_label")
    search_fields = ("tx_hash","from_address","to_address")
    list_filter = ("is_anomaly","risk_label")

admin.site.register(Batch)
admin.site.register(WalletProfile)
