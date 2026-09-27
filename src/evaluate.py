"""
Part B4 — Evaluation stage.

Loads the trained model and processed test set, computes test loss and
accuracy, generates a confusion-matrix image, and writes metrics.json
at the project root so DVC can track it as a metric.

Run standalone with:
    python src/evaluate.py
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.models import load_model

PROCESSED_DIR = os.path.join("data", "processed")
MODELS_DIR = "models"
METRICS_PATH = "metrics.json"
CONF_MATRIX_PATH = os.path.join(MODELS_DIR, "confusion_matrix.png")

CLASS_NAMES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot",
]


def main():
    test_data = np.load(os.path.join(PROCESSED_DIR, "test.npz"))
    x_test, y_test = test_data["images"], test_data["labels"]

    model = load_model(os.path.join(MODELS_DIR, "model.h5"))

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)

    y_pred = np.argmax(model.predict(x_test, verbose=0), axis=1)
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(8, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_NAMES)
    disp.plot(ax=ax, xticks_rotation=45, colorbar=False)
    plt.tight_layout()
    plt.savefig(CONF_MATRIX_PATH)
    plt.close(fig)

    metrics = {"test_loss": float(test_loss), "test_accuracy": float(test_acc)}
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Test loss: {test_loss:.4f} | Test accuracy: {test_acc:.4f}")
    print(f"Confusion matrix saved to {CONF_MATRIX_PATH}")
    print(f"Metrics saved to {METRICS_PATH}")


if __name__ == "__main__":
    main()
