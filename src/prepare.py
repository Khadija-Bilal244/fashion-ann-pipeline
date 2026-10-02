"""
Part B1 — Data preparation stage.

Loads Fashion-MNIST directly from tf.keras.datasets and dumps the raw
train/test arrays to data/raw/ as .npz files. No hyperparameters are
needed at this stage, so params.yaml is not read here.

Run standalone with:
    python src/prepare.py
"""

import os

import numpy as np
from keras.datasets import fashion_mnist

RAW_DIR = os.path.join("data", "raw")


def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

    np.savez_compressed(
        os.path.join(RAW_DIR, "train.npz"), images=x_train, labels=y_train
    )
    np.savez_compressed(
        os.path.join(RAW_DIR, "test.npz"), images=x_test, labels=y_test
    )

    print(f"Saved raw train arrays: {x_train.shape}, {y_train.shape}")
    print(f"Saved raw test arrays:  {x_test.shape}, {y_test.shape}")
    print(f"Written to: {RAW_DIR}/train.npz and {RAW_DIR}/test.npz")


if __name__ == "__main__":
    main()
