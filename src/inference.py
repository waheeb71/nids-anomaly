from typing import Dict
import numpy as np
import pandas as pd
from preprocess import transform_single, transform_df, load_scaler
from models import load_if, load_ocsvm, load_ae
from config import IF_THRESHOLD, OCSVM_THRESHOLD, AE_RECON_ERROR, FEATURES
from datetime import datetime

class AnomalyDetector:
    def __init__(self):
        self.scaler = load_scaler()
        self.if_model = load_if()
        self.ocsvm_model = load_ocsvm()
        try:
            self.ae = load_ae()
            self.ae_loaded = True
        except Exception:
            self.ae = None
            self.ae_loaded = False

    def predict_single(self, sample: Dict) -> Dict:
        # تحويل البيانات وتقييسها
        x = transform_single(sample, scaler=self.scaler).reshape(1, -1)

        # Isolation Forest
        if_score = self.if_model.decision_function(x)[0]
        if_anomaly = int(if_score < IF_THRESHOLD)

        # One-Class SVM
        oc_score = self.ocsvm_model.decision_function(x)[0]
        oc_anomaly = int(oc_score < OCSVM_THRESHOLD)

        # Autoencoder
        ae_score = None
        ae_anomaly = 0
        if self.ae_loaded:
            recon = self.ae.predict(x, verbose=0)
            mse = float(np.mean((x - recon) ** 2))
            ae_score = mse
            ae_anomaly = int(mse > AE_RECON_ERROR)

        # القرار النهائي: True إذا أي نموذج كشف شذوذ
        votes = [if_anomaly, oc_anomaly, ae_anomaly]
        final_anomaly = int(sum(votes) >= 2)

        # قيمة timestamp افتراضية إذا لم تكن موجودة
        timestamp = sample.get('timestamp', datetime.now().timestamp())
        src_ip = sample.get('src_ip', 'unknown')
        src_port = sample.get('src_port', 'unknown')

        # Host compromised flag
        host_compromised = final_anomaly and sum(votes) >= 2  # تعديل حسب حاجتك

        result = {
            'timestamp': timestamp,
            'src_ip': src_ip,
            'src_port': src_port,
            'if_score': float(if_score),
            'if_anomaly': bool(if_anomaly),
            'oc_score': float(oc_score),
            'oc_anomaly': bool(oc_anomaly),
            'ae_score': ae_score,
            'ae_anomaly': bool(ae_anomaly),
            'final_anomaly': bool(final_anomaly),
            'window_anomaly_count': 0,  # يمكن تعديله لاحقًا إذا استخدمت نافذة
            'host_compromised': bool(host_compromised)
        }

        # طباعة التنبيهات
        if result['final_anomaly']:
            print(f"[ALERT] Packet from {src_ip}:{src_port} detected as anomaly!")
        if result['host_compromised']:
            print(f"[CRITICAL] Host {src_ip} flagged as compromised!")

        return result

    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        X = transform_df(df, scaler=self.scaler).values

        # Isolation Forest
        if_scores = self.if_model.decision_function(X)
        if_dec = (if_scores < IF_THRESHOLD).astype(int)

        # One-Class SVM
        oc_scores = self.ocsvm_model.decision_function(X)
        oc_dec = (oc_scores < OCSVM_THRESHOLD).astype(int)

        # Autoencoder
        ae_scores = None
        ae_dec = np.zeros(len(X), dtype=int)
        if self.ae_loaded:
            recons = self.ae.predict(X, verbose=0)
            mses = np.mean((X - recons) ** 2, axis=1)
            ae_scores = mses
            ae_dec = (mses > AE_RECON_ERROR).astype(int)

        # القرار النهائي
        final = ((if_dec + oc_dec + ae_dec) >= 2).astype(int)
        host_compromised = final.copy()  # أو حسب منطقك

        out = df.copy()
        out['timestamp'] = df.get('timestamp', pd.Series([datetime.now().timestamp()]*len(df)))
        out['src_ip'] = df.get('src_ip', 'unknown')
        out['src_port'] = df.get('src_port', 'unknown')
        out['if_score'] = if_scores
        out['if_anomaly'] = if_dec
        out['oc_score'] = oc_scores
        out['oc_anomaly'] = oc_dec
        if ae_scores is not None:
            out['ae_score'] = ae_scores
            out['ae_anomaly'] = ae_dec
        out['final_anomaly'] = final
        out['window_anomaly_count'] = 0
        out['host_compromised'] = host_compromised

        # طباعة التنبيهات لكل صف
        for i, row in out.iterrows():
            if row['final_anomaly']:
                print(f"[ALERT] Packet from {row['src_ip']}:{row['src_port']} detected as anomaly!")
            if row['host_compromised']:
                print(f"[CRITICAL] Host {row['src_ip']} flagged as compromised!")

        return out
