from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Transaction
from apps.ml_engine.ml_manager import score_transaction

@shared_task(bind=True)
def async_score_transaction(self, transaction_id: str):
    try:
        tx = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return {"status":"not_found", "id": transaction_id}

    result = score_transaction(tx)  # returns dict with scores
    # update DB
    tx.anomaly_score = result.get("anomaly_score")
    tx.is_anomaly = result.get("is_anomaly", False)
    tx.risk_score = result.get("risk_score")
    tx.risk_label = result.get("risk_label", "unknown")
    tx.metadata.update(result.get("metadata", {}))
    tx.save()
    return {"status":"scored", "id": transaction_id}
