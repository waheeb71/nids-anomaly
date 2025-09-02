from collections import deque
import time
from typing import Dict, List
from features import extract_features_from_packet
from inference import AnomalyDetector

class RealTimeNIDS:
    def __init__(self, window_size: int = 50, use_window: bool = True, threshold: int = 3):
        """
        window_size: عدد الحزم التي تُخزن في النافذة.
        use_window: تفعيل/تعطيل نافذة التتبع.
        threshold: عدد الحزم الشاذة لتحديد المضيف كمخترق.
        """
        self.detector = AnomalyDetector()
        self.use_window = use_window
        self.threshold = threshold
        self.window = deque(maxlen=window_size)

    def process_packet(self, packet: Dict) -> Dict:
        # استخراج الميزات من الحزمة
        features = extract_features_from_packet(packet)

        # التنبؤ باستخدام جميع النماذج
   
        result = self.detector.predict_single(features)

        # إضافة معلومات إضافية
        result_out = {
            "timestamp": time.time(),
            "src_ip": packet.get("src_ip"),
            "src_port": packet.get("src_port"),
            **result
        }

        # تحديث النافذة إذا مفعلة
        if self.use_window:
            self.window.append(result_out["final_anomaly"])
            window_anomalies = sum(self.window)
            host_compromised = window_anomalies >= self.threshold
            result_out["window_anomaly_count"] = window_anomalies
            result_out["host_compromised"] = host_compromised
        else:
            result_out["window_anomaly_count"] = 0
            result_out["host_compromised"] = False

        # تحسين العرض: طباعة تنبيه إن وجد
        if result_out["final_anomaly"]:
            print(f"[ALERT] Packet from {result_out['src_ip']}:{result_out['src_port']} detected as anomaly!")
        elif self.use_window and result_out["host_compromised"]:
            print(f"[CRITICAL] Host {result_out['src_ip']} flagged as compromised!")

        return result_out

    def process_batch(self, packets: List[Dict]) -> List[Dict]:
        """
        معالجة مجموعة من الحزم دفعة واحدة
        """
        results = []
        for pkt in packets:
            results.append(self.process_packet(pkt))
        return results


