import os
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from tensorflow.keras import layers, models
from joblib import dump, load
from src.config import MODEL_DIR, IF_PATH, OCSVM_PATH, AE_PATH

def train_isolation_forest(X, **kwargs):
    clf = IsolationForest(n_estimators=200, contamination=0.01, random_state=42, **kwargs)
    clf.fit(X)
    os.makedirs(MODEL_DIR, exist_ok=True)
    dump(clf, IF_PATH)
    return clf

def train_oneclass_svm(X, **kwargs):
    clf = OneClassSVM(kernel='rbf', gamma='auto', nu=0.01, **kwargs)
    clf.fit(X)
    dump(clf, OCSVM_PATH)
    return clf

def build_autoencoder(input_dim:int, latent_dim:int=16):
    inp = layers.Input(shape=(input_dim,))
    x = layers.Dense(64, activation='relu')(inp)
    x = layers.Dense(32, activation='relu')(x)
    latent = layers.Dense(latent_dim, activation='relu')(x)
    x = layers.Dense(32, activation='relu')(latent)
    x = layers.Dense(64, activation='relu')(x)
    out = layers.Dense(input_dim, activation='linear')(x)
    ae = models.Model(inputs=inp, outputs=out)
    ae.compile(optimizer='adam', loss='mse')
    return ae

def train_autoencoder(X, epochs=50, batch_size=256):
    ae = build_autoencoder(X.shape[1])
    ae.fit(X, X, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=2)
    ae.save(AE_PATH)
    return ae

def load_if():
    return load(IF_PATH)

def load_ocsvm():
    return load(OCSVM_PATH)

def load_ae():
    from tensorflow.keras.models import load_model
    return load_model(AE_PATH)
