

import pandas as pd
from src.preprocess import fit_scaler, transform_df
from src.models import train_isolation_forest, train_oneclass_svm, train_autoencoder
from src.config import FEATURES

def run(path_to_training_csv: str):
    df = pd.read_csv(path_to_training_csv)
    df = df.dropna(subset=FEATURES)
    scaler = fit_scaler(df)
    X = transform_df(df, scaler=scaler).values
   
    train_isolation_forest(X)
    train_oneclass_svm(X)
    train_autoencoder(X, epochs=30)

if __name__ == '__main__':
    import sys
    run(sys.argv[1])
