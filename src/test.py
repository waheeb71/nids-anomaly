from realtime import RealTimeNIDS

import random
from datetime import datetime

nids = RealTimeNIDS(window_size=10, threshold=3)


packets = []


for i in range(20):
    pkt = {
        "src_ip": f"10.0.{random.randint(1,5)}.{random.randint(1,254)}",
        "src_port": random.randint(1024, 65535),
        "bytes_fwd": random.randint(100, 2000),
        "bytes_bwd": random.randint(50, 500),
        "pkts_fwd": random.randint(1, 50),
        "pkts_bwd": random.randint(1, 50),
        "duration_ms": random.randint(50, 500),
        "pkt_len_mean": random.randint(40, 150),
        "pkt_len_std": random.randint(5, 30),
        "pkt_len_max": random.randint(100, 200),
        "pkt_len_min": random.randint(20, 50),
        "pkt_rate": random.randint(10, 200),
        "byte_rate": random.randint(100, 2000),
        "syn_count": random.randint(0,2),
        "fin_count": random.randint(0,1),
        "rst_count": random.randint(0,1),
        "psh_count": random.randint(0,2),
        "ack_count": random.randint(0,5),
        "retransmissions": random.randint(0,2),
        "out_of_order": random.randint(0,1),
        "small_pkt_ratio": random.random(),
        "idle_time_mean": random.random()*5,
        "fwd_bwd_ratio_bytes": random.uniform(0.5, 2.0),
        "fwd_bwd_ratio_pkts": random.uniform(0.5, 2.0),
        "timestamp": datetime.now().timestamp()
    }
    packets.append(pkt)


for i in range(5):
    pkt = {
        "src_ip": "10.0.1.50",
        "src_port": random.randint(1024, 65535),
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
        "timestamp": datetime.now().timestamp()
    }
    packets.append(pkt)


results = nids.process_batch(packets)


for r in results:
    print(r)
