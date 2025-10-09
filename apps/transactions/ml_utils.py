# apps/transactions/ml_utils.py
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler
import joblib
from pathlib import Path
from django.conf import settings
from datetime import datetime

class EnhancedMLModelManager:
    def __init__(self):
        self.model = None
        self.scaler = RobustScaler()
        self.model_path = Path(settings.BASE_DIR) / 'ml_models' / 'isolation_forest_v2.joblib'

    def extract_advanced_features(self, transaction_data):
        features = []
        amount = float(transaction_data.get('amount', 0) or 0)
        fee = float(transaction_data.get('fee', 0) or 0)

        # log scaled amount and fee
        features.append(np.log1p(amount))
        features.append(np.log1p(fee))

        # fee ratio
        fee_ratio = (fee / amount * 100) if amount > 0 else 0
        features.append(fee_ratio)

        # amount bucket
        if amount < 0.01:
            amount_category = 0
        elif amount < 0.1:
            amount_category = 1
        elif amount < 1:
            amount_category = 2
        elif amount < 10:
            amount_category = 3
        elif amount < 100:
            amount_category = 4
        else:
            amount_category = 5
        features.append(amount_category)

        # round indicator
        is_round = 1 if amount == int(amount) and amount > 0 else 0
        features.append(is_round)

        # time-based features
        ts = transaction_data.get('timestamp')
        if ts is None:
            features.extend([0.5, 0.5, 0, 0])
        else:
            try:
                ts = pd.to_datetime(ts)
                features.append(ts.hour / 23.0)
                features.append(ts.weekday() / 6.0)
                features.append(1 if ts.weekday() >= 5 else 0)
                features.append(1 if ts.hour < 6 or ts.hour > 22 else 0)
            except Exception:
                features.extend([0.5, 0.5, 0, 0])
        return features

    def train_model(self, transactions_df):
        X = []
        for _, row in transactions_df.iterrows():
            X.append(self.extract_advanced_features(row))
        X = np.array(X)
        X_scaled = self.scaler.fit_transform(X)
        self.model = IsolationForest(
            contamination=0.15,
            random_state=42,
            n_estimators=150,
            n_jobs=-1
        )
        self.model.fit(X_scaled)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({'model': self.model, 'scaler': self.scaler, 'trained_at': datetime.now().isoformat()}, self.model_path)
        return self.model

    def load_model(self):
        if self.model_path.exists():
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data.get('scaler', self.scaler)
            return True
        return False

    def predict(self, transaction_data):
        if self.model is None and not self.load_model():
            return self._default_prediction()
        features = self.extract_advanced_features(transaction_data)
        X_scaled = self.scaler.transform([features])
        pred = int(self.model.predict(X_scaled)[0])
        anomaly_score = float(self.model.score_samples(X_scaled)[0])
        risk_score = self._calculate_risk_score(anomaly_score)
        return {
            'is_anomaly': (pred == -1),
            'risk_score': risk_score,
            'anomaly_score': anomaly_score,
            'confidence': abs(anomaly_score)
        }

    def _calculate_risk_score(self, anomaly_score):
        # map typical scores to 0-100
        risk_score = int((anomaly_score + 0.5) * 100)
        return max(0, min(100, risk_score))

    def _default_prediction(self):
        return {'is_anomaly': False, 'risk_score': 50, 'anomaly_score': 0.0, 'confidence': 0.0}
