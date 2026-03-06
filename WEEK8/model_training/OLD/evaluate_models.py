import pandas as pd
import joblib
import json

from sklearn.metrics import classification_report, confusion_matrix

# ================================
# PATHS
# ================================

TEST_PATH = "WEEK7/output/test_dataset.csv"
MODEL_PATH = "WEEK8/model_training/best_model.pkl"
LABEL_MAP_PATH = "WEEK7/output/label_mapping.json"

METADATA_COLS = ['source_file', 'error_category', 'line_number', 'column_number', 'label']

# ================================
# LOAD DATA
# ================================

test_df = pd.read_csv(TEST_PATH)

# feature_cols = [c for c in test_df.columns if c not in METADATA_COLS]



FEATURE_COLUMNS_PATH = "WEEK8/model_training/feature_columns.json"

with open(FEATURE_COLUMNS_PATH) as f:
    feature_cols = json.load(f)

X_test = test_df[feature_cols]
y_test = test_df['label']
model = joblib.load(MODEL_PATH)

with open(LABEL_MAP_PATH) as f:label_map = json.load(f)

# ================================
# PREDICTION
# ================================

preds = model.predict(X_test)

# ================================
# METRICS
# ================================

print("\nClassification Report\n")
print(classification_report(y_test, preds, target_names=label_map.values()))

print("\nConfusion Matrix\n")
print(confusion_matrix(y_test, preds))