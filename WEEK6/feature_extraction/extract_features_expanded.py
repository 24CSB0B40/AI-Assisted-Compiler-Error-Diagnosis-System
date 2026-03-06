"""
Week 7 - Feature Extraction for Expanded Dataset
Extracts 28 ML features from the augmented 496-row dataset.
"""

import pandas as pd
import re
from pathlib import Path
import os

INPUT_CSV  = "WEEK7/output/augmented_dataset.csv"
OUTPUT_CSV = "WEEK6/feature_extraction/output/features_dataset_expanded.csv"

SOURCE_DIRS = [
    "WEEK5/error_collection/sample_programs"
]

def analyze_error_message(error_message):
    message = str(error_message).lower()
    return {
        'msg_has_expected':     1 if 'expected' in message else 0,
        'msg_has_declared':     1 if ('declared' in message or 'undeclared' in message) else 0,
        'msg_has_before':       1 if 'before' in message else 0,
        'msg_has_type':         1 if 'type' in message else 0,
        'msg_has_conversion':   1 if ('conversion' in message or 'convert' in message) else 0,
        'msg_has_return':       1 if 'return' in message else 0,
        'msg_has_control':      1 if 'control' in message else 0,
        'msg_has_implicit':     1 if 'implicit' in message else 0,
        'msg_has_unknown':      1 if 'unknown' in message else 0,
        'msg_mentions_semicolon': 1 if ("';'" in str(error_message) or 'semicolon' in message) else 0,
        'msg_mentions_brace':   1 if ("'{'" in str(error_message) or "'}'" in str(error_message) or 'brace' in message) else 0,
        'msg_mentions_paren':   1 if ("'('" in str(error_message) or "')'" in str(error_message) or 'parenthes' in message) else 0,
        'msg_length':           len(str(error_message)),
        'msg_word_count':       len(str(error_message).split()),
    }

def read_code_line(source_file, line_number):
    # Strip augmentation suffix for file lookup
    base_file = str(source_file)
    if '_aug' in base_file:
        # e.g. missing_semicolon_5_aug123.cpp -> missing_semicolon_5.cpp
        base_file = re.sub(r'_aug\d+\.cpp$', '.cpp', base_file)
    
    for src_dir in SOURCE_DIRS:
        file_path = Path(src_dir) / base_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                ln = int(line_number)
                if 1 <= ln <= len(lines):
                    return lines[ln - 1].strip()
            except:
                pass
    return ""

def analyze_code_line(source_file, line_number):
    code_line = read_code_line(source_file, line_number)
    if not code_line:
        return {
            'code_length': 0, 'code_ends_semicolon': 0,
            'code_has_declaration': 0, 'code_open_braces': 0,
            'code_close_braces': 0, 'code_open_parens': 0,
            'code_close_parens': 0, 'code_has_assignment': 0,
            'code_has_comparison': 0, 'code_has_string': 0,
        }
    type_kw = r'\b(int|float|double|char|bool|void|long|short|string|unsigned|const)\b'
    return {
        'code_length':          len(code_line),
        'code_ends_semicolon':  1 if code_line.endswith(';') else 0,
        'code_has_declaration': 1 if re.search(type_kw, code_line) else 0,
        'code_open_braces':     code_line.count('{'),
        'code_close_braces':    code_line.count('}'),
        'code_open_parens':     code_line.count('('),
        'code_close_parens':    code_line.count(')'),
        'code_has_assignment':  1 if ('=' in code_line and '==' not in code_line) else 0,
        'code_has_comparison':  1 if any(op in code_line for op in ['==','!=','<','>','<=','>=']) else 0,
        'code_has_string':      1 if ('"' in code_line or "'" in code_line) else 0,
    }

def extract_features(row):
    msg_f  = analyze_error_message(row['error_message'])
    code_f = analyze_code_line(row['source_file'], row['line_number'])
    bal_f  = {
        'brace_balance': code_f['code_open_braces'] - code_f['code_close_braces'],
        'paren_balance': code_f['code_open_parens'] - code_f['code_close_parens'],
        'total_braces':  code_f['code_open_braces'] + code_f['code_close_braces'],
        'total_parens':  code_f['code_open_parens'] + code_f['code_close_parens'],
    }
    return {
        'source_file':      row['source_file'],
        'error_category':   row['error_category'],
        'line_number':      row['line_number'],
        'column_number':    row['column_number'],
        **msg_f, **code_f, **bal_f
    }

def main():
    print(f"\n{'='*60}")
    print("  FEATURE EXTRACTION — EXPANDED DATASET")
    print(f"{'='*60}")
    
    df = pd.read_csv(INPUT_CSV)
    print(f"  Loading {len(df)} rows...\n")
    
    all_features = []
    for idx, row in df.iterrows():
        if (idx + 1) % 100 == 0:
            print(f"  Progress: {idx+1}/{len(df)}")
        all_features.append(extract_features(row))
    
    features_df = pd.DataFrame(all_features)
    features_df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n  ✔ Saved: {OUTPUT_CSV}")
    print(f"  Rows: {len(features_df)}")
    print(f"  Columns: {len(features_df.columns)} (4 metadata + 28 ML features)")
    print(f"\n  Class distribution:")
    for cat, count in sorted(features_df['error_category'].value_counts().items()):
        print(f"    {cat:<42} {count}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
