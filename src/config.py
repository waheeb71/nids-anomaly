FEATURES = [
    'bytes_fwd','bytes_bwd','pkts_fwd','pkts_bwd','duration_ms',
    'pkt_len_mean','pkt_len_std','pkt_len_max','pkt_len_min','pkt_rate','byte_rate',
    'syn_count','fin_count','rst_count','psh_count','ack_count',
    'retransmissions','out_of_order','small_pkt_ratio','idle_time_mean',
    'fwd_bwd_ratio_bytes','fwd_bwd_ratio_pkts'
]

MODEL_DIR = 'models'
SCALER_PATH = MODEL_DIR + '/scaler.joblib'
IF_PATH = MODEL_DIR + '/isolation_forest.joblib'
OCSVM_PATH = MODEL_DIR + '/oneclass_svm.joblib'
AE_PATH = MODEL_DIR + '/autoencoder.h5'

IF_THRESHOLD = -0.2
OCSVM_THRESHOLD = 0.0
AE_RECON_ERROR = 0.01
