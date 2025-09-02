from typing import Dict
from config import FEATURES

def extract_features_from_packet(packet: Dict) -> Dict:
    f = {k: float(packet.get(k, 0.0)) for k in FEATURES}
 
    try:
        if f.get('pkts_bwd', 0) == 0:
            f['fwd_bwd_ratio_pkts'] = float('inf') if f.get('pkts_fwd',0)>0 else 1.0
    except Exception:
        f['fwd_bwd_ratio_pkts'] = 1.0
    try:
        if f.get('bytes_bwd', 0) == 0:
            f['fwd_bwd_ratio_bytes'] = float('inf') if f.get('bytes_fwd',0)>0 else 1.0
    except Exception:
        f['fwd_bwd_ratio_bytes'] = 1.0
    return f
