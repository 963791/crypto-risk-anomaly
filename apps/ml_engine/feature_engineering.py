import pandas as pd
from datetime import datetime

def featurize_row(row: dict) -> dict:
    # minimal example features — expand with domain knowledge
    ts = row.get("timestamp")
    try:
        hour = pd.to_datetime(ts).hour
    except Exception:
        hour = 0
    amount = float(row.get("amount", 0))
    # example derived features
    log_amount = 0.0
    if amount > 0:
        import math
        log_amount = math.log(amount + 1)
    # placeholder: one-hot encodes or hash addresses to numeric features in production
    return {
        "amount": amount,
        "log_amount": log_amount,
        "hour": hour,
    }

def featurize_dataframe(df):
    feats = df.apply(lambda r: pd.Series(featurize_row(r)), axis=1)
    return feats
