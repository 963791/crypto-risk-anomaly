import shap
import joblib
from pathlib import Path
import numpy as np
from .feature_engineering import featurize_dataframe

ARTIFACT_DIR = Path(__file__).resolve().parent.parent.parent / "ml_models"

def explain_instance(instance_row):
    model_file = ARTIFACT_DIR / "risk_model_v1.joblib"
    if not model_file.exists():
        return {"error": "model not found"}
    model = joblib.load(model_file)
    X = featurize_dataframe(instance_row.to_frame().T)
    explainer = shap.Explainer(model.predict_proba if hasattr(model, "predict_proba") else model.predict, X)
    shap_values = explainer(X)
    return {"shap_values": shap_values.values.tolist(), "features": X.columns.tolist()}
