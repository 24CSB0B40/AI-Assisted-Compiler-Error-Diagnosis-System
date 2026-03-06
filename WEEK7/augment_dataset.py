"""
Week 7 - Data Augmentation
Expands the 376-row real dataset to ~500 samples through
controlled synthetic augmentation.

Strategy:
- Only augment categories that are underrepresented
- Augmentation = vary line_number, column_number, error_message wording
- Label (error_category) is preserved exactly
- Never invent new error patterns — only vary surface features
"""

import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

INPUT_CSV  = r"D:\ACADEMICS\SEM_4\COMPILER DESIGN\LAB\AI-Compiler-Error-Diagnosis\WEEK5\error_collection\output\collected_errors.csv"
OUTPUT_CSV = r"D:\ACADEMICS\SEM_4\COMPILER DESIGN\LAB\AI-Compiler-Error-Diagnosis\WEEK7\output\augmented_dataset.csv"

TARGET_PER_CLASS = 62  # aim for ~62 per category * 8 = 496 ≈ 500

# ─────────────────────────────────────────────────────────
# Synonym maps for augmentation — varies wording slightly
# ─────────────────────────────────────────────────────────

MESSAGE_VARIATIONS = {
    # Replace tokens in error messages with equivalent phrasing
    "expected ';'":         ["expected a semicolon ';'", "expected ';' token"],
    "before":               ["prior to", "before token"],
    "not declared":         ["was not declared", "undeclared identifier"],
    "in this scope":        ["in current scope", "within this scope"],
    "control reaches end":  ["control reaches end of function", "reaches end of non-void"],
    "non-void function":    ["non-void function without return", "non-void return type"],
    "unknown type name":    ["unknown type", "unrecognized type name"],
    "invalid conversion":   ["invalid type conversion", "cannot convert"],
    "incompatible types":   ["type mismatch", "incompatible type assignment"],
    "implicit declaration": ["implicit function declaration", "undeclared function"],
}

def augment_message(message):
    """Apply a small random variation to an error message."""
    msg = message
    # Pick one substitution at random if applicable
    candidates = [(k, v) for k, v in MESSAGE_VARIATIONS.items() if k in msg.lower()]
    if candidates:
        key, replacements = random.choice(candidates)
        replacement = random.choice(replacements)
        msg = msg.lower().replace(key, replacement, 1)
    return msg

def augment_row(row):
    """Create a synthetic variant of a real error row."""
    new_row = row.copy()
    
    # Vary line number by ±1-5 lines
    delta = random.randint(1, 5)
    new_row['line_number'] = max(1, int(row['line_number']) + random.choice([-1, 1]) * delta)
    
    # Vary column number by ±1-3
    delta_col = random.randint(1, 3)
    new_row['column_number'] = max(1, int(row['column_number']) + random.choice([-1, 1]) * delta_col)
    
    # Slightly vary the error message
    new_row['error_message'] = augment_message(str(row['error_message']))
    
    # Mark as augmented in source_file name
    base = str(row['source_file']).replace('.cpp', '').replace('.c', '')
    new_row['source_file'] = f"{base}_aug{random.randint(100,999)}.cpp"
    
    return new_row

def main():
    print(f"\n{'='*60}")
    print("  DATA AUGMENTATION")
    print(f"{'='*60}")
    
    df = pd.read_csv(INPUT_CSV)
    print(f"  Original dataset:  {len(df)} rows")
    
    class_counts = df['error_category'].value_counts()
    print(f"\n  Class distribution (before augmentation):")
    for cat, count in sorted(class_counts.items()):
        print(f"    {cat:<42} {count:>4}")
    
    augmented_rows = []
    
    for category in df['error_category'].unique():
        cat_df = df[df['error_category'] == category]
        current_count = len(cat_df)
        needed = max(0, TARGET_PER_CLASS - current_count)
        
        if needed > 0:
            # Sample rows to augment (with replacement if needed)
            source_rows = cat_df.sample(n=needed, replace=True, random_state=42)
            for _, row in source_rows.iterrows():
                augmented_rows.append(augment_row(row))
            print(f"  + Augmented '{category}': +{needed} rows")
        else:
            print(f"    '{category}': already has {current_count} rows (no augmentation needed)")
    
    aug_df = pd.DataFrame(augmented_rows)
    final_df = pd.concat([df, aug_df], ignore_index=True)
    
    # Shuffle
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    final_df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n{'='*60}")
    print(f"  AUGMENTATION COMPLETE")
    print(f"{'='*60}")
    print(f"  Original rows:   {len(df)}")
    print(f"  Augmented rows:  {len(aug_df)}")
    print(f"  Final total:     {len(final_df)}")
    
    final_counts = final_df['error_category'].value_counts()
    print(f"\n  Final class distribution:")
    for cat, count in sorted(final_counts.items()):
        pct = count / len(final_df) * 100
        print(f"    {cat:<42} {count:>4} ({pct:4.1f}%)")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
