import pandas as pd
import joblib
import json
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ================================
# PATHS
# ================================

TRAIN_PATH           = "WEEK7/output/train_dataset.csv"
TEST_PATH            = "WEEK7/output/test_dataset.csv"
MODEL_OUTPUT         = "WEEK8/model_training/best_model.pkl"
FEATURE_COLUMNS_PATH = "WEEK8/model_training/feature_columns.json"
RESULTS_OUTPUT       = "WEEK8/model_training/all_model_results.json"

os.makedirs("WEEK8/model_training", exist_ok=True)

METADATA_COLS = ['source_file', 'error_category', 'line_number', 'column_number', 'label']

# ================================
# LOAD DATA
# ================================

print("\nLoading datasets...")

train_df = pd.read_csv(TRAIN_PATH)
test_df  = pd.read_csv(TEST_PATH)

# Only keep numeric feature columns
feature_cols = train_df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Remove label column from features
if 'label' in feature_cols:
    feature_cols.remove('label')

# Save feature schema for evaluate_models.py to reuse
with open(FEATURE_COLUMNS_PATH, "w") as f:
    json.dump(feature_cols, f)

print("Feature schema saved.")

X_train = train_df[feature_cols]
y_train = train_df['label']

X_test  = test_df[feature_cols]
y_test  = test_df['label']

print(f"Training samples : {len(X_train)}")
print(f"Test samples     : {len(X_test)}\n")

# ================================
# DEFINE MODELS
# ================================

models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),

    "SVM": SVC(
        kernel='rbf',
        probability=True,
        random_state=42
    ),

    "Logistic Regression": LogisticRegression(
        max_iter=10000,
        random_state=42
    ),

    "KNN": KNeighborsClassifier(
        n_neighbors=5
    )
}

# ================================
# TRAIN & EVALUATE ALL MODELS
# ================================

results    = {}
best_model = None
best_score = 0
best_name  = ""

for name, model in models.items():

    print(f"Training {name}...")

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc   = accuracy_score(y_test, preds)

    results[name] = round(acc, 4)

    print(f"  Accuracy: {acc:.4f}\n")

    if acc > best_score:
        best_score = acc
        best_model = model
        best_name  = name

# ================================
# SAVE BEST MODEL
# ================================

joblib.dump(best_model, MODEL_OUTPUT)

# ================================
# SAVE ALL RESULTS TO FILE
# ================================

with open(RESULTS_OUTPUT, "w") as f:
    json.dump({
        "best_model": best_name,
        "best_accuracy": round(best_score, 4),
        "all_model_accuracies": results
    }, f, indent=2)

print("-"*60)
print(f"Best Model   : {best_name}")
print(f"Best Accuracy: {best_score:.4f}")
print(f"Model saved  : {MODEL_OUTPUT}")
print(f"Results saved: {RESULTS_OUTPUT}")
print("-"*60)
