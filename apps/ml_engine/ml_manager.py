from pathlib import Path
import joblib
import numpy as np
from .feature_engineering import featurize_row, featurize_dataframe

ARTIFACT_DIR = Path(__file__).resolve().parent.parent.parent / "ml_models"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

ISO_FILE = ARTIFACT_DIR / "isolation_forest_v1.joblib"
RISK_FILE = ARTIFACT_DIR / "risk_model_v1.joblib"

def load_models():
    models = {}
    if ISO_FILE.exists():
        models["iso"] = joblib.load(ISO_FILE)
    if RISK_FILE.exists():
        models["risk"] = joblib.load(RISK_FILE)
    return models

def score_transaction_sync(tx_obj):
    """Synchronous scoring for small volumes."""
    feat = featurize_row({
        "amount": float(tx_obj.amount),
        "timestamp": tx_obj.timestamp.isoformat(),
        "from_address": tx_obj.from_address,
        "to_address": tx_obj.to_address,
    })
    X = np.array([list(feat.values())])
    models = load_models()
    res = {}
    if "iso" in models:
        iso = models["iso"]
        # anomaly score: negative outlier factor (sklearn IsolationForest.score_samples gives +ve for inliers)
        an_score = -float(iso.score_samples(X)[0])
        res["anomaly_score"] = an_score
        res["is_anomaly"] = an_score > 0.5
    if "risk" in models:
        risk = models["risk"]
        if hasattr(risk, "predict_proba"):
            proba = float(risk.predict_proba(X)[0][1])
        else:
            proba = float(risk.predict(X)[0])
        res["risk_score"] = proba
        res["risk_label"] = "high" if proba > 0.75 else ("medium" if proba > 0.4 else "low")
    res["metadata"] = {"features": feat}
    return res

def score_transaction(tx_obj):
    # wrapper that calls sync function (used by Celery)
    return score_transaction_sync(tx_obj)
