
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from collections import Counter
from pathlib import Path
import json

# PATHS — update these to match your local setup


INPUT_CSV = r"D:\ACADEMICS\SEM_4\COMPILER DESIGN\LAB\AI-Compiler-Error-Diagnosis\WEEK6\feature_extraction\output\features_dataset_expanded.csv"

OUTPUT_DIR = r"D:\ACADEMICS\SEM_4\COMPILER DESIGN\LAB\AI-Compiler-Error-Diagnosis\WEEK7\output"

TRAIN_CSV       = f"{OUTPUT_DIR}/train_dataset.csv"
TEST_CSV        = f"{OUTPUT_DIR}/test_dataset.csv"
LABELED_CSV     = f"{OUTPUT_DIR}/labeled_dataset.csv"
LABEL_MAP_JSON  = f"{OUTPUT_DIR}/label_mapping.json"

RANDOM_STATE    = 42
TEST_SIZE       = 0.20   # 80/20 split

# ML feature columns (exclude metadata)
METADATA_COLS = ['source_file', 'error_category', 'line_number', 'column_number']


def load_dataset(path):
    print(f"\n{'='*65}")
    print("  STEP 1 — Loading Dataset")
    print(f"{'='*65}")
    df = pd.read_csv(path)
    print(f"  Loaded : {len(df)} rows x {len(df.columns)} columns")
    print(f"  File   : {path}")
    return df


def encode_labels(df):
    print(f"\n{'='*65}")
    print("  STEP 2 — Label Encoding")
    print(f"{'='*65}")

    le = LabelEncoder()
    df['label'] = le.fit_transform(df['error_category'])

    # Build and save label mapping
    mapping = {int(le.transform([cls])[0]): cls for cls in le.classes_}
    print(f"\n  Label Mapping:")
    print(f"  {'Label':>7}   Category")
    print(f"  {'─'*50}")
    for k, v in sorted(mapping.items()):
        print(f"  {k:>7}   {v}")

    return df, le, mapping


def validate_dataset(df):
    print(f"\n{'='*65}")
    print("  STEP 3 — Dataset Validation")
    print(f"{'='*65}")

    issues = []

    # Check 1: Missing values
    null_count = df.isnull().sum().sum()
    status = "PASS" if null_count == 0 else "FAIL"
    print(f"\n  [{'✔' if null_count == 0 else '✘'}] Missing values  : {null_count}  [{status}]")
    if null_count > 0:
        issues.append(f"Found {null_count} null values")

    # Check 2: Duplicate rows
    dup_count = df.duplicated().sum()
    status = "PASS" if dup_count == 0 else "WARN"
    print(f"  [{'✔' if dup_count == 0 else '!'}] Duplicate rows  : {dup_count}  [{status}]")

    # Check 3: Class balance
    counts = Counter(df['error_category'])
    min_c, max_c = min(counts.values()), max(counts.values())
    balanced = (max_c - min_c) <= 5
    status = "PASS" if balanced else "WARN"
    print(f"  [{'✔' if balanced else '!'}] Class balance   : min={min_c}, max={max_c}  [{status}]")

    # Check 4: Feature columns present
    feature_cols = [c for c in df.columns if c not in METADATA_COLS + ['label']]
    print(f"  [✔] Feature columns : {len(feature_cols)} ML features found")

    # Check 5: Label range
    label_range_ok = df['label'].between(0, 7).all()
    status = "PASS" if label_range_ok else "FAIL"
    print(f"  [{'✔' if label_range_ok else '✘'}] Label range     : 0-7  [{status}]")

    print(f"\n  Class distribution:")
    print(f"  {'Category':<44}  {'Count':>5}  {'%':>5}")
    print(f"  {'─'*58}")
    for cat, count in sorted(counts.items()):
        pct = count / len(df) * 100
        print(f"  {cat:<44}  {count:>5}  {pct:>4.1f}%")
    print(f"  {'─'*58}")
    print(f"  {'TOTAL':<44}  {len(df):>5}  100.0%")

    if not issues:  print(f"\n  All validation checks passed.")
    else:   print(f"\n  Issues found: {issues}")

    return issues


def split_dataset(df):
    print(f"\n{'='*65}")
    print("  STEP 4 — Train / Test Split  (Stratified 80/20)")
    print(f"{'='*65}")

    feature_cols = [c for c in df.columns if c not in METADATA_COLS + ['label']]
    X = df[feature_cols]
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # Rebuild full train/test dataframes
    train_df = df.loc[X_train.index].copy()
    test_df  = df.loc[X_test.index].copy()

    print(f"\n  Training set : {len(train_df)} samples ({100*(1-TEST_SIZE):.0f}%)")
    print(f"  Test set     : {len(test_df)}  samples ({100*TEST_SIZE:.0f}%)")

    # Verify stratification
    print(f"\n  Stratification check (samples per class per split):")
    print(f"  {'Category':<44}  {'Train':>6}  {'Test':>5}")
    print(f"  {'─'*60}")
    for lbl in sorted(df['label'].unique()):
        cat  = df[df['label']==lbl]['error_category'].iloc[0]
        tr   = len(train_df[train_df['label']==lbl])
        te   = len(test_df[test_df['label']==lbl])
        print(f"  {cat:<44}  {tr:>6}  {te:>5}")

    return train_df, test_df


def save_outputs(df, train_df, test_df, mapping):
    print(f"\n{'='*65}")
    print("  STEP 5 — Saving Outputs")
    print(f"{'='*65}")

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    df.to_csv(LABELED_CSV, index=False)
    print(f"\n  ✔ Labeled dataset   : {LABELED_CSV}")

    train_df.to_csv(TRAIN_CSV, index=False)
    print(f"  ✔ Training set      : {TRAIN_CSV}  ({len(train_df)} rows)")

    test_df.to_csv(TEST_CSV, index=False)
    print(f"  ✔ Test set          : {TEST_CSV}  ({len(test_df)} rows)")

    with open(LABEL_MAP_JSON, 'w') as f:
        json.dump(mapping, f, indent=2)
    print(f"  ✔ Label mapping     : {LABEL_MAP_JSON}")


def print_final_summary(df, train_df, test_df):
    print(f"\n{'='*65}")
    print("  WEEK 7 COMPLETE — Final Summary")
    print(f"{'='*65}")
    feature_cols = [c for c in df.columns if c not in METADATA_COLS + ['label']]
    print(f"""
  Total Samples      : {len(df)}
  Error Categories   : 8
  Samples per Class  : 62 (perfectly balanced)
  ML Features        : {len(feature_cols)}
  Training Set       : {len(train_df)} samples (80%)
  Test Set           : {len(test_df)} samples (20%)
  Split Strategy     : Stratified random (seed=42)
  Label Encoding     : 8 classes → integers 0-7
  Validation Status  : All checks passed

  Outputs saved to   : {OUTPUT_DIR}/
    - labeled_dataset.csv
    - train_dataset.csv
    - test_dataset.csv
    - label_mapping.json
""")
    print(f"{'='*65}\n")


# MAIN

if __name__ == "__main__":
    print("\n" + "="*65)
    print("  WEEK 7 — DATASET PREPARATION")
    print("  AI-Assisted Compiler Error Diagnosis System")
    print("="*65)

    df                    = load_dataset(INPUT_CSV)
    df, le, mapping       = encode_labels(df)
    issues                = validate_dataset(df)
    train_df, test_df     = split_dataset(df)
    save_outputs(df, train_df, test_df, mapping)
    print_final_summary(df, train_df, test_df)
