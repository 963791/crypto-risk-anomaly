from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaction, Batch
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from apps.transactions.tasks import async_score_transaction

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["from_address","to_address","is_anomaly","risk_label"]

    def perform_create(self, serializer):
        tx = serializer.save()
        # enqueue scoring task (Celery)
        try:
            async_score_transaction.delay(str(tx.id))
        except Exception:
            # fallback: do in-process (small datasets)
            from apps.ml_engine.ml_manager import score_transaction_sync
            score_transaction_sync(tx)
