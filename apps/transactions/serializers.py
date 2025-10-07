from rest_framework import serializers
from .models import Transaction, Batch, WalletProfile

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ("anomaly_score","is_anomaly","risk_score","risk_label","created_at")
