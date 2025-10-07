from .feature_engineering import featurize_dataframe
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

ARTIFACT_DIR = Path(__file__).resolve().parent.parent.parent / "ml_models"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

def train_and_persist_models(df):
    # df expected to have `label` column (1 risky, 0 ok) for supervised model
    X = featurize_dataframe(df)
    X_values = X.values

    # Isolation Forest for anomalies (unsupervised)
    iso = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
    iso.fit(X_values)
    joblib.dump(iso, ARTIFACT_DIR / "isolation_forest_v1.joblib")

    if "label" in df.columns:
        y = df["label"].astype(int).values
        pipe = Pipeline([("scaler", StandardScaler()), ("clf", RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42))])
        pipe.fit(X_values, y)
        joblib.dump(pipe, ARTIFACT_DIR / "risk_model_v1.joblib")
    return True
