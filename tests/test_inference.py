import pytest
from src.inference import AnomalyDetector

def test_predict_single_smoke():
    det = AnomalyDetector()
    sample = {k: 0.0 for k in det.scaler.feature_names_in_} if hasattr(det.scaler, 'feature_names_in_') else { }
    # create minimal sample using feature names from config fallback
    from src.config import FEATURES
    sample = {k: 0.0 for k in FEATURES}
    res = det.predict_single(sample)
    assert 'final_anomaly' in res
