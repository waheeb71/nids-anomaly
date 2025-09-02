

# Real-Time Network Intrusion Detection System (NIDS) with Anomaly Detection

## Overview

This project implements a **real-time Network Intrusion Detection System (NIDS)** using **machine learning-based anomaly detection**. It monitors network traffic, extracts relevant features from packets, and detects anomalous activity that may indicate attacks or compromised hosts.

The system combines multiple detection models to improve accuracy:
- **Isolation Forest (IF)** – Detects anomalies based on feature distribution.
- **One-Class SVM (OCSVM)** – Identifies unusual patterns using a support vector approach.
- **Autoencoder (AE)** – Measures reconstruction error to spot abnormal packet behavior.

The final decision is based on a **voting mechanism**: a packet is flagged as anomalous if at least two models agree. A **sliding window** tracks recent anomalies to determine if a host is potentially compromised.

---

## How It Works

1. **Packet Capture and Feature Extraction**  
   Each network packet is processed to extract numerical features such as:
   - Packet size statistics (mean, min, max)
   - Forward/backward packet counts and byte ratios
   - Flags counts (SYN, ACK, FIN, RST, PSH)
   - Retransmissions and out-of-order packets
   - Packet rate, byte rate, small packet ratio, idle time
   - Forward/backward ratios for bytes and packets  

2. **Anomaly Detection**  
   Extracted features are fed to the **AnomalyDetector**, which runs the three models:
   - **Isolation Forest:** outputs `if_score` and `if_anomaly`.
   - **One-Class SVM:** outputs `oc_score` and `oc_anomaly`.
   - **Autoencoder (optional):** outputs `ae_score` and `ae_anomaly`.

3. **Final Voting and Host Assessment**  
   - A packet is marked as anomalous if at least two models flag it (`final_anomaly = True`).
   - A sliding window counts recent anomalies. If the number exceeds the threshold, the host is flagged as compromised (`host_compromised = True`).

4. **Real-Time Processing**  
   The system can process packets individually (`process_packet`) or in batches (`process_batch`). Alerts are printed in real-time for anomalous packets and compromised hosts.

---


# NIDS Anomaly Detection System

## Project Overview

This project implements a **real-time Network Intrusion Detection System (NIDS)** using machine learning models to detect anomalous network traffic that may indicate cyber-attacks. It is designed to identify suspicious packets or flows and flag potentially compromised hosts.

The system combines multiple models:

- **Isolation Forest (IF)** – detects deviations from normal traffic patterns.
- **One-Class SVM (OCSVM)** – identifies packets outside the learned normal boundary.
- **Autoencoder (AE)** – reconstructs normal patterns; high reconstruction errors indicate anomalies.

A **voting mechanism** aggregates model predictions. If 2 or more models flag a packet as anomalous, the system marks it as suspicious.

Optionally, a **sliding window** tracks recent anomalies per host to detect ongoing attacks.

---
## Features Used

The system extracts the following 22 features from each packet or flow:

| Feature | Description | Why it matters |
|---------|-------------|----------------|
| `bytes_fwd` | Number of bytes sent forward | High or low values may indicate abnormal transfers or exfiltration. |
| `bytes_bwd` | Number of bytes received | Unusually high or low traffic can signal scanning or floods. |
| `pkts_fwd` | Number of packets sent forward | Sudden spikes may indicate flooding attacks. |
| `pkts_bwd` | Number of packets received | High incoming packets can signal DDoS or scanning. |
| `duration_ms` | Duration of the flow in milliseconds | Very short or long durations can indicate abnormal behavior. |
| `pkt_len_mean` | Mean packet length | Abnormal average size may indicate unusual payloads. |
| `pkt_len_std` | Standard deviation of packet lengths | High variability may indicate bursty attacks. |
| `pkt_len_max` | Maximum packet length | Extremely large packets may be malicious. |
| `pkt_len_min` | Minimum packet length | Very small packets can be part of flooding or probing attacks. |
| `pkt_rate` | Packets per second | Sudden increases can indicate DoS, scanning, or botnet activity. |
| `byte_rate` | Bytes per second | High throughput may indicate exfiltration or volumetric attacks. |
| `syn_count` | Number of SYN flags | High SYN counts may indicate SYN flood attacks. |
| `fin_count` | Number of FIN flags | Unusual FIN behavior may indicate stealth scanning. |
| `rst_count` | Number of RST flags | Excessive resets can signal session disruption attacks. |
| `psh_count` | Number of PSH flags | Can highlight bursts of unusual application data. |
| `ack_count` | Number of ACK flags | Abnormal patterns may indicate backscatter or flooding. |
| `retransmissions` | Number of retransmitted packets | High retransmissions may indicate network issues or attacks. |
| `out_of_order` | Count of out-of-order packets | Significant disorder may indicate scanning or replay attacks. |
| `small_pkt_ratio` | Ratio of small packets | Flooding attacks often involve many small packets. |
| `idle_time_mean` | Average idle time between packets | Very short or long idle times may reveal anomalous behavior. |
| `fwd_bwd_ratio_bytes` | Ratio of forward to backward bytes | Extreme asymmetry can indicate exfiltration or scanning. |
| `fwd_bwd_ratio_pkts` | Ratio of forward to backward packets | Identifies imbalanced flows or attacks. |

---

## How the System Detects Attacks

1. **Feature Transformation & Scaling**  
   Each packet’s features are normalized to ensure consistent ranges.

2. **Model Predictions**  
   - **Isolation Forest:** Detects outliers in the feature space.  
   - **One-Class SVM:** Flags points outside the normal data boundary.  
   - **Autoencoder:** Flags flows that the model cannot accurately reconstruct.

3. **Voting Mechanism**  
   - If **2 or more models** predict a packet as anomalous → `final_anomaly = True`.

4. **Sliding Window (Optional)**  
   - Counts recent anomalies for each host.  
   - If anomalies exceed the `threshold` → `host_compromised = True`.

---

## Project Structure

```

nids-anomaly/
│
├─ src/
│  └─ a.py                # Example script to test detection
│
├─ features.py            # Extract features from network packets
├─ inference.py           # Anomaly detection models
├─ realtime.py            # Real-time NIDS implementation
└─ README.md              # This file

````

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/waheeb/nids-anomaly.git
cd nids-anomaly
````

2. Create and activate a Python virtual environment:

```bash
python3 -m venv ai_env
source ai_env/bin/activate    # On Linux/Mac
ai_env\Scripts\activate       # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---
## Training the Model

The models can be retrained on your own dataset (e.g., `large_train_with_ip.csv`).
The dataset should contain network traffic features such as packet sizes, flow duration, rates, flags, etc.

1. Place your training dataset (CSV) in the project folder.
2. Run the training script:

```bash
python scripts/train_all.py data/large_train_with_ip.csv
```

---
## Usage

### 1. Test a single packet

```python
from inference import AnomalyDetector

detector = AnomalyDetector()
sample_packet = {
    "src_ip": "10.1.2.3",
    "src_port": 12345,
    "bytes_fwd": 1500,
    "bytes_bwd": 200,
    "pkts_fwd": 30,
    "pkts_bwd": 10,
    "duration_ms": 200,
    "pkt_len_mean": 80,
    "pkt_len_std": 15,
    "pkt_len_max": 120,
    "pkt_len_min": 60,
    "pkt_rate": 50,
    "byte_rate": 1000,
    "syn_count": 1,
    "fin_count": 0,
    "rst_count": 0,
    "psh_count": 0,
    "ack_count": 2,
    "retransmissions": 0,
    "out_of_order": 0,
    "small_pkt_ratio": 0.1,
    "idle_time_mean": 1,
    "fwd_bwd_ratio_bytes": 1.5,
    "fwd_bwd_ratio_pkts": 2.0
}

result = detector.predict_single(sample_packet)
print(result)
```

### 2. Real-time packet processing

```python
from realtime import RealTimeNIDS
import time

nids = RealTimeNIDS(window_size=10, threshold=3)

# Example packet
packet = {
    "src_ip": "10.0.1.50",
    "src_port": 12345,
    "bytes_fwd": 10000,
    "bytes_bwd": 5000,
    "pkts_fwd": 200,
    "pkts_bwd": 100,
    "duration_ms": 10,
    "pkt_len_mean": 500,
    "pkt_len_std": 100,
    "pkt_len_max": 1500,
    "pkt_len_min": 400,
    "pkt_rate": 1000,
    "byte_rate": 50000,
    "syn_count": 10,
    "fin_count": 0,
    "rst_count": 5,
    "psh_count": 10,
    "ack_count": 20,
    "retransmissions": 5,
    "out_of_order": 3,
    "small_pkt_ratio": 0.9,
    "idle_time_mean": 0.1,
    "fwd_bwd_ratio_bytes": 5.0,
    "fwd_bwd_ratio_pkts": 4.0,
    "timestamp": time.time()
}

result = nids.process_packet(packet)
print(result)
```

### 3. Processing multiple packets

```python
packets = [packet1, packet2, packet3, ...]
results = nids.process_batch(packets)
for res in results:
    print(res)
```

---
## How to Interpret Results

* `final_anomaly = True` → Packet is flagged as suspicious.
* `host_compromised = True` → Host is flagged as potentially compromised due to repeated anomalies.
* `if_score`, `oc_score`, `ae_score` → Scores from each model.
* `window_anomaly_count` → Number of anomalies in the recent window.

---

## Model Training

The anomaly detection models are **pre-trained** using normal network traffic data. The training steps are:

1. **Data Preprocessing**

   * Extract features for each packet.
   * Standardize the features using `StandardScaler`.

2. **Model Training**

   * **Isolation Forest (IF):** trained on normal traffic to learn feature distributions.
   * **One-Class SVM (OCSVM):** trained on normal traffic to define the boundary of normal behavior.
   * **Autoencoder (AE):** trained to reconstruct normal traffic; large reconstruction errors indicate anomalies.

3. **Thresholds**

   * `IF_THRESHOLD`, `OCSVM_THRESHOLD`, `AE_RECON_ERROR` are determined from the training set to balance false positives and detection rate.

Once trained, the models are saved and loaded during runtime.

---

## Key Features

* Real-time packet anomaly detection.
* Multiple model ensemble with voting mechanism.
* Sliding window to track host compromise over time.
* Easy integration into live network monitoring systems.
* Printable alerts for quick incident response.

---

## Notes

* Ensure TensorFlow/Keras is installed if using the Autoencoder model.
* The sliding window improves detection of persistent anomalies but can be disabled.
* Adjust `window_size` and `threshold` to tune sensitivity.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---
##  Contact:
For questions or support, contact me via:
- Telegram: [@SyberSc71](https://t.me/SyberSc71)
- Telegram: [@WAT4F](https://t.me/WAT4F)
- GitHub: [waheeb71](https://github.com/waheeb71)
- GitHub2: [cyberlangdev](https://github.com/cyberlangdev)
- **Location:** I am from Yemen, Taiz.
- **YouTube Channel:** [Cyber Code](https://www.youtube.com/@cyber_code1)
- **X (formerly Twitter):** [@wa__cys](https://x.com/wa__cys)

---
## Author / المطور

**English:** Waheeb Mahyoob Al-Sharabi (Waheeb Al-Sharabi)  
**العربية:** هيب مهيوب الشرعبي (هيب الشرعبي)