"""
Part B3 — Training stage.

Builds a fully-connected ANN (Flatten -> Dense/ReLU -> Dropout ->
Dense(10, softmax)), compiles it with Adam + sparse_categorical_crossentropy,
trains it on data/processed/, and saves the model and training history.

Hyperparameters come from params.yaml -> train.

Run standalone with:
    python src/train.py
"""

import os

import numpy as np
import pandas as pd
import yaml
from tensorflow.keras import layers, models, optimizers

PROCESSED_DIR = os.path.join("data", "processed")
MODELS_DIR = "models"


def load_params(path="params.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def build_model(dense_units, dropout_rate, learning_rate):
    model = models.Sequential(
        [
            layers.Flatten(input_shape=(28, 28)),
            layers.Dense(dense_units, activation="relu"),
            layers.Dropout(dropout_rate),
            layers.Dense(10, activation="softmax"),
        ]
    )
    model.compile(
        optimizer=optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    params = load_params()["train"]
    os.makedirs(MODELS_DIR, exist_ok=True)

    train_data = np.load(os.path.join(PROCESSED_DIR, "train.npz"))
    val_data = np.load(os.path.join(PROCESSED_DIR, "val.npz"))

    model = build_model(
        dense_units=params["dense_units"],
        dropout_rate=params["dropout_rate"],
        learning_rate=params["learning_rate"],
    )
    model.summary()

    history = model.fit(
        train_data["images"],
        train_data["labels"],
        validation_data=(val_data["images"], val_data["labels"]),
        epochs=params["epochs"],
        batch_size=params["batch_size"],
        verbose=2,
    )

    model.save(os.path.join(MODELS_DIR, "model.h5"))

    hist_df = pd.DataFrame(history.history)
    hist_df.index.name = "epoch"
    hist_df.to_csv(os.path.join(MODELS_DIR, "history.csv"))

    print(f"Model saved to {MODELS_DIR}/model.h5")
    print(f"History saved to {MODELS_DIR}/history.csv")


if __name__ == "__main__":
    main()
