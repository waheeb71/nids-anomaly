

# AI-Powered Real-Time Network Intrusion Detection System (NIDS)

## Overview
This project is a **real-time AI-based network intrusion detection system** designed to monitor network traffic, detect anomalies, and identify potentially compromised hosts. It leverages machine learning models to analyze network packets and provide timely alerts to prevent security incidents.

**Key Features:**
- Real-time packet monitoring
- Multi-model anomaly detection (Isolation Forest, One-Class models, Autoencoder)
- Host compromise detection based on anomaly thresholds
- Configurable window for tracking consecutive anomalies
- Extensible and easy to integrate with existing network infrastructure

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

## How it Works

1. **Packet Feature Extraction**: Raw network packets are converted into measurable features.
2. **Anomaly Detection**: Each packet is evaluated by multiple AI models to determine if it is anomalous.
3. **Window Tracking**: Consecutive anomalies are tracked per host. If the threshold is exceeded, the host is flagged as compromised.
4. **Alerts**: Real-time alerts are printed for detected anomalies or compromised hosts.

---

## License

MIT License

---





