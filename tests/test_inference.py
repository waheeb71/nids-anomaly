import pytest
import numpy as np
from src.inference import AnomalyDetector
from src.config import FEATURES


@pytest.fixture(scope="module")
def detector():
    return AnomalyDetector()


@pytest.fixture
def sample_packet():
    """Generate a minimal valid sample with zeros."""
    return {k: 0.0 for k in FEATURES}


def test_predict_single_returns_expected_keys(detector, sample_packet):
    """Ensure predict_single returns all expected fields."""
    res = detector.predict_single(sample_packet)
    expected_keys = {
        "if_score", "if_anomaly",
        "oc_score", "oc_anomaly",
        "ae_score", "ae_anomaly",
        "final_anomaly"
    }
    assert expected_keys.issubset(res.keys())


def test_predict_single_anomaly_flag_type(detector, sample_packet):
    """Check anomaly flags are booleans or int (0/1)."""
    res = detector.predict_single(sample_packet)
    assert isinstance(res["final_anomaly"], (bool, np.bool_, int))


def test_predict_batch_multiple_samples(detector, sample_packet):
    """Test batch predictions return list with consistent structure."""
    samples = [sample_packet.copy() for _ in range(5)]
    results = detector.predict_batch(samples)
    assert isinstance(results, list)
    assert len(results) == 5
    assert all("final_anomaly" in r for r in results)


def test_predict_single_with_random_values(detector):
    """Smoke test with non-zero values."""
    sample = {k: np.random.rand() * 100 for k in FEATURES}
    res = detector.predict_single(sample)
    assert "final_anomaly" in res
    assert isinstance(res["final_anomaly"], (bool, np.bool_, int))


def test_models_work_individually(detector, sample_packet):
    """Directly test internal models."""
    X = np.array([[sample_packet[k] for k in FEATURES]])
    
    # Isolation Forest
    if hasattr(detector, "iforest"):
        _ = detector.iforest.decision_function(X)
        _ = detector.iforest.predict(X)

    # One-Class SVM
    if hasattr(detector, "ocsvm"):
        _ = detector.ocsvm.decision_function(X)
        _ = detector.ocsvm.predict(X)

    # Autoencoder
    if hasattr(detector, "autoencoder"):
        _ = detector.autoencoder.predict(X)


def test_scaler_transform(detector, sample_packet):
    """Ensure scaler can transform inputs."""
    X = np.array([[sample_packet[k] for k in FEATURES]])
    X_scaled = detector.scaler.transform(X)
    assert X_scaled.shape == X.shape
