# fashion-ann-pipeline

End-to-end, DVC-versioned TensorFlow ANN pipeline that classifies
Fashion-MNIST images into 10 clothing categories, targeting ≥85% test
accuracy. Reproducible in one command: `dvc repro`.

## Project layout

```
fashion-ann-pipeline/
├── data/
│   ├── raw/                # output of prepare.py (DVC-tracked)
│   └── processed/          # output of preprocess.py (DVC-tracked)
├── models/                 # model.h5, history.csv, confusion_matrix.png (DVC-tracked)
├── src/
│   ├── prepare.py          # B1 — load Fashion-MNIST, save raw arrays
│   ├── preprocess.py       # B2 — normalize + train/val split
│   ├── train.py            # B3 — build/train the ANN
│   └── evaluate.py         # B4 — test metrics + confusion matrix
├── params.yaml              # all hyperparameters (D1)
├── dvc.yaml                  # 4-stage pipeline definition (D2)
├── metrics.json              # produced by evaluate.py, tracked as a DVC metric
├── requirements.txt
└── .gitignore
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Running the pipeline

```bash
dvc repro
```

This runs `prepare -> preprocess -> train -> evaluate` in order, skipping
any stage whose dependencies/params haven't changed since the last run.

## DVC remote (Google Drive)

See `GUIDE.md` for the full, copy-pasteable walkthrough of every Git and
DVC step in the assignment (Parts A–E), including Google Drive OAuth setup
and the merge-conflict simulation.
