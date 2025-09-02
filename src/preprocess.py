import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
from src.config import FEATURES, SCALER_PATH, MODEL_DIR

def fit_scaler(df: pd.DataFrame):
    scaler = StandardScaler()
    scaler.fit(df[FEATURES].values)
    os.makedirs(MODEL_DIR, exist_ok=True)
    dump(scaler, SCALER_PATH)
    return scaler

def load_scaler():
    return load(SCALER_PATH)

def transform_df(df: pd.DataFrame, scaler=None):
    if scaler is None:
        scaler = load_scaler()
    arr = scaler.transform(df[FEATURES].values)
    return pd.DataFrame(arr, columns=FEATURES, index=df.index)

def transform_single(sample: dict, scaler=None):
    import pandas as pd
    if scaler is None:
        scaler = load_scaler()
    df = pd.DataFrame([[sample.get(f,0.0) for f in FEATURES]], columns=FEATURES)
    arr = scaler.transform(df.values)
    return arr[0]
