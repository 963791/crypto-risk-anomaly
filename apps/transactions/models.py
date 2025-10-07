from django.db import models
import uuid
from django.conf import settings

class Batch(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name or str(self.id)

class WalletProfile(models.Model):
    address = models.CharField(max_length=128, unique=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.address

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    tx_hash = models.CharField(max_length=128, unique=True)
    from_address = models.CharField(max_length=128)
    to_address = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=30, decimal_places=8)
    fee = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    timestamp = models.DateTimeField()
    # ML outputs
    anomaly_score = models.FloatField(null=True, blank=True)
    is_anomaly = models.BooleanField(default=False)
    risk_score = models.FloatField(null=True, blank=True)
    risk_label = models.CharField(max_length=32, default="unknown")
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.tx_hash
