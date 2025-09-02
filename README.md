
# Real-Time Network Intrusion Detection System (NIDS) with Anomaly Detection
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.12-orange?logo=tensorflow&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2-lightgrey?logo=scikitlearn&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-waheeb71-black?logo=github&logoColor=white)
## Overview

This project implements a **real-time Network Intrusion Detection System (NIDS)** using **machine learning-based anomaly detection**.  
It monitors network traffic, extracts relevant features from packets, and detects anomalous activity that may indicate attacks or compromised hosts.

The system combines multiple models for higher accuracy:
**Models Used:**
- 🟢 **Isolation Forest (IF)** – Detects anomalies based on feature distributions.  
- 🔵 **One-Class SVM (OCSVM)** – Identifies unusual patterns using a support vector approach.  
- 🟠 **Autoencoder (AE)** – Measures reconstruction error to spot abnormal packet behavior.



A **voting mechanism** flags a packet as anomalous if at least two models agree.  
A **sliding window** tracks recent anomalies to detect potentially compromised hosts over time.

> **Benefit:** Early detection of attacks minimizes downtime and prevents data exfiltration or malicious network activity.

---

## Features

The system extracts **22 features** from each packet or flow:

| Feature | Description | Why it matters |
|---------|-------------|----------------|
| `bytes_fwd` | Bytes sent forward | Abnormally high or low may indicate data exfiltration or scanning. |
| `bytes_bwd` | Bytes received | Sudden spikes can signal scanning or flooding attacks. |
| `pkts_fwd` | Packets sent forward | Flooding or DoS attacks may cause spikes. |
| `pkts_bwd` | Packets received | Excessive incoming packets can indicate attacks. |
| `duration_ms` | Flow duration in milliseconds | Very short/long flows can be suspicious. |
| `pkt_len_mean` | Average packet length | Unusual payload sizes may be malicious. |
| `pkt_len_std` | Std deviation of packet lengths | High variability indicates bursty attacks. |
| `pkt_len_max` | Maximum packet length | Extremely large packets may be malicious. |
| `pkt_len_min` | Minimum packet length | Very small packets can indicate probing/flooding. |
| `pkt_rate` | Packets per second | Rapid packet sending may indicate DoS or scanning. |
| `byte_rate` | Bytes per second | High throughput may indicate exfiltration or volumetric attacks. |
| `syn_count` | Number of SYN flags | High counts can indicate SYN floods. |
| `fin_count` | Number of FIN flags | Abnormal FIN behavior may indicate stealth scans. |
| `rst_count` | Number of RST flags | Excessive resets can disrupt sessions. |
| `psh_count` | Number of PSH flags | Highlights bursts of unusual application data. |
| `ack_count` | Number of ACK flags | Unusual patterns may indicate backscatter or flooding. |
| `retransmissions` | Number of retransmitted packets | High retransmissions may indicate network issues or attacks. |
| `out_of_order` | Out-of-order packet count | Can indicate scanning, replay attacks, or network instability. |
| `small_pkt_ratio` | Ratio of small packets | Flooding attacks often use many small packets. |
| `idle_time_mean` | Average idle time between packets | Very short/long idle times reveal anomalies. |
| `fwd_bwd_ratio_bytes` | Forward/backward byte ratio | Extreme asymmetry can signal exfiltration or scanning. |
| `fwd_bwd_ratio_pkts` | Forward/backward packet ratio | Imbalanced flows may indicate attacks. |

---

## How It Works

1. **Packet Capture & Feature Extraction**  
   Extract numerical features from each packet/flow.

2. **Anomaly Detection** via `AnomalyDetector`:  
   - 🟢 Isolation Forest → `if_score`, `if_anomaly`  
   - 🔵 One-Class SVM → `oc_score`, `oc_anomaly`  
   - 🟠 Autoencoder → `ae_score`, `ae_anomaly` 
   
3. **Voting Mechanism**  
   - Packet flagged as anomalous if **2 or more models** agree (`final_anomaly = True`).

4. **Sliding Window**  
   - Tracks anomalies per host.  
   - Host flagged if anomalies exceed threshold (`host_compromised = True`).

5. **Real-Time Processing**  
   - `process_packet()` for single packets  
   - `process_batch()` for multiple packets  
   - Alerts printed in real-time for anomalous packets and compromised hosts.

---

## Installation

```bash
git clone https://github.com/waheeb/nids-anomaly.git
cd nids-anomaly
python3 -m venv ai_env
source ai_env/bin/activate    # Linux/Mac
ai_env\Scripts\activate       # Windows
pip install -r requirements.txt
````

---

## Training the Models

Models can be retrained on custom datasets (CSV format with network traffic features).

```bash
python scripts/train_all.py data/large_train_with_ip.csv
```

**Training Steps:**

1. Preprocess & standardize features (`StandardScaler`).
2. Train models on normal traffic:

   * Isolation Forest
   * One-Class SVM
   * Autoencoder
3. Set thresholds (`IF_THRESHOLD`, `OCSVM_THRESHOLD`, `AE_RECON_ERROR`) from training data.
4. Save models for runtime usage.

---

## Usage

### Test Single Packet

```python
from inference import AnomalyDetector

detector = AnomalyDetector()
sample_packet = { ... }  # packet features
result = detector.predict_single(sample_packet)
print(result)
```

### Real-Time Packet Processing

```python
from realtime import RealTimeNIDS
import time

nids = RealTimeNIDS(window_size=10, threshold=3)
packet = { ... }
result = nids.process_packet(packet)
print(result)
```

### Batch Processing

```python
packets = [packet1, packet2, packet3, ...]
results = nids.process_batch(packets)
for res in results:
    print(res)
```

---

## Interpreting Results

* `final_anomaly = True` → Packet flagged as suspicious.
* `host_compromised = True` → Host potentially compromised.
* `if_score`, `oc_score`, `ae_score` → Model-specific scores.
* `window_anomaly_count` → Number of anomalies in recent window.

---

## Project Structure

```
nids-anomaly/
│
├─ src/
│  └─ a.py                # Example detection script
├─ features.py            # Feature extraction from packets
├─ inference.py           # Anomaly detection models
├─ realtime.py            # Real-time NIDS
└─ README.md              # Project documentation
```

---

## Notes

* Ensure **TensorFlow/Keras** installed for Autoencoder.
* Sliding window improves detection of persistent anomalies; can be disabled.
* Adjust `window_size` and `threshold` for sensitivity.

---

## License

MIT License – see [LICENSE](LICENSE).

---

## Contact

* **Telegram:** [@SyberSc71](https://t.me/SyberSc71), [@WAT4F](https://t.me/WAT4F)
* **GitHub:** [waheeb71](https://github.com/waheeb71), [cyberlangdev](https://github.com/cyberlangdev)
* **YouTube:** [Cyber Code](https://www.youtube.com/@cyber_code1)
* **X / Twitter:** [@wa\_\_cys](https://x.com/wa__cys)
* **Location:** Taiz, Yemen

---

## Author / المطور

**English:** Waheeb Mahyoob Al-Sharabi
**العربية:** هيب مهيوب الشرعبي

```

---

