import pandas as pd
import numpy as np
import joblib
import json
import os

from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# ================================
# PATHS
# ================================

TRAIN_PATH           = "WEEK7/output/train_dataset.csv"
TEST_PATH            = "WEEK7/output/test_dataset.csv"
MODEL_PATH           = "WEEK8/model_training/best_model.pkl"
LABEL_MAP_PATH       = "WEEK7/output/label_mapping.json"
FEATURE_COLUMNS_PATH = "WEEK8/model_training/feature_columns.json"
RESULTS_OUTPUT       = "WEEK8/evaluation/best_model_evaluation.json"

os.makedirs("WEEK8/evaluation", exist_ok=True)

METADATA_COLS = ['source_file', 'error_category', 'line_number', 'column_number', 'label']

# ================================
# LOAD DATA
# ================================

train_df = pd.read_csv(TRAIN_PATH)
test_df  = pd.read_csv(TEST_PATH)

# Load saved feature schema from train_models.py
with open(FEATURE_COLUMNS_PATH) as f:
    feature_cols = json.load(f)

# Load label mapping - sorted by numeric key to guarantee correct order
with open(LABEL_MAP_PATH) as f:
    label_map = json.load(f)

class_names = [label_map[str(k)] for k in sorted(int(k) for k in label_map.keys())]

X_train = train_df[feature_cols].values
X_test  = test_df[feature_cols].values
y_train = train_df['label'].values
y_test  = test_df['label'].values

# Full dataset used for cross-validation
X_full = np.vstack([X_train, X_test])
y_full = np.concatenate([y_train, y_test])

model = joblib.load(MODEL_PATH)

# ================================
# PREDICTION
# ================================

preds = model.predict(X_test)

# ================================
# PRECISION & RECALL
# ================================

accuracy  = accuracy_score(y_test, preds)
precision = precision_score(y_test, preds, average='weighted', zero_division=0)
recall    = recall_score(y_test, preds,    average='weighted', zero_division=0)
f1        = f1_score(y_test, preds,        average='weighted', zero_division=0)

print("\n" + "="*60)
print("  CORE METRICS (Weighted Average)")
print("="*60)
print(f"  Accuracy  : {accuracy:.4f}")
print(f"  Precision : {precision:.4f}")
print(f"  Recall    : {recall:.4f}")
print(f"  F1-Score  : {f1:.4f}")

# ================================
# CLASSIFICATION REPORT
# ================================

print("\n" + "="*60)
print("  CLASSIFICATION REPORT")
print("="*60)
print(classification_report(y_test, preds, target_names=class_names, zero_division=0))

# Also capture as dict for saving to file
report_dict = classification_report(
    y_test, preds,
    target_names=class_names,
    zero_division=0,
    output_dict=True
)

# ================================
# CONFUSION MATRIX (LABELED)
# ================================

cm    = confusion_matrix(y_test, preds)
cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)

print("="*60)
print("  CONFUSION MATRIX  (Rows = Actual, Columns = Predicted)")
print("="*60)
print(cm_df.to_string())
print()

# ================================
# CROSS-VALIDATION (5-FOLD)
# ================================

cv        = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X_full, y_full, cv=cv, scoring='accuracy')

print("="*60)
print("  5-FOLD CROSS-VALIDATION")
print("="*60)
print(f"  Fold Scores : {[round(s, 4) for s in cv_scores]}")
print(f"  Mean        : {cv_scores.mean():.4f}")
print(f"  Std Dev     : {cv_scores.std():.4f}")

# ================================
# SAVE RESULTS TO FILE
# ================================

evaluation_results = {
    "model": type(model).__name__,
    "test_samples": int(len(X_test)),
    "core_metrics": {
        "accuracy":  round(float(accuracy),  4),
        "precision": round(float(precision), 4),
        "recall":    round(float(recall),    4),
        "f1_score":  round(float(f1),        4)
    },
    "cross_validation": {
        "n_folds": 5,
        "scores":  [round(float(s), 4) for s in cv_scores],
        "mean":    round(float(cv_scores.mean()), 4),
        "std":     round(float(cv_scores.std()),  4)
    },
    "classification_report": report_dict,
    "confusion_matrix": {
        "labels": class_names,
        "matrix": cm.tolist()
    }
}

with open(RESULTS_OUTPUT, "w") as f:
    json.dump(evaluation_results, f, indent=2)

print("\n" + "-"*60)
print(f"Results saved: {RESULTS_OUTPUT}")
print("-"*60)
