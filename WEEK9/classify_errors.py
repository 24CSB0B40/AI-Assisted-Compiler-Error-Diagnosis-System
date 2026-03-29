
"""
HOW TO RUN:
    python classify_errors.py <your_file.cpp>

EXAMPLE:
    python classify_errors.py missing_semicolon_1.cpp
    python classify_errors.py mycode.cpp
"""

import subprocess   # To run g++ compiler
import re           # Regex for parsing error messages
import sys          # For command-line arguments
import json         # To load label_mapping and feature_columns
import joblib       # To load the trained ML model
import os           # File existence checks
from pathlib import Path  # File path handling



# SECTION 1: CONFIGURATION — FILE PATHS

MODEL_PATH         = "WEEK8/model_training/best_model.pkl"
FEATURE_COLS_PATH  = "WEEK8/model_training/feature_columns.json"
LABEL_MAP_PATH     = "WEEK7/output/label_mapping.json"


# SECTION 2: LOAD MODEL + METADATA

def load_model_and_metadata():
    """
    Load the trained Random Forest model, feature column order,
    and label mapping from disk.

    Returns:
        model        - trained sklearn RandomForestClassifier
        feature_cols - list of feature names in correct order
        label_map    - dict mapping predicted int → category name
    """

    # Check all required files exist before loading
    for path in [MODEL_PATH, FEATURE_COLS_PATH, LABEL_MAP_PATH]:
        if not os.path.exists(path):
            print(f"\n  ERROR: Required file not found → {path}")
            print("  Make sure Week 7 and Week 8 outputs are present.\n")
            sys.exit(1)

    model        = joblib.load(MODEL_PATH)
    
    with open(FEATURE_COLS_PATH) as f:
        feature_cols = json.load(f)

    with open(LABEL_MAP_PATH) as f:
        label_map = json.load(f)

    return model, feature_cols, label_map


# SECTION 3: COMPILE THE FILE AND CAPTURE ERRORS

def compile_and_capture(filepath):
    """
    Run g++ on the given file and capture error output.

    Parameters:
        filepath (str) - path to the .cpp or .c file

    Returns:
        error output string if errors exist, else None
    """

    ext      = Path(filepath).suffix
    compiler = 'gcc' if ext == '.c' else 'g++'

    # Windows-compatible temp file instead of /dev/null
    import tempfile
    tmp_file = tempfile.NamedTemporaryFile(suffix='.o', delete=False)
    tmp_path = tmp_file.name
    tmp_file.close()

    try:
        result = subprocess.run(
        [compiler, '-Werror=return-type', '-c', filepath, '-o', tmp_path],
        capture_output=True,
        text=True,
        timeout=5
        )

        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

        if result.returncode != 0:
            return result.stderr   # Has errors → return them
        else:
            return None            # Compiled successfully

    except subprocess.TimeoutExpired:
        print("  ERROR: Compilation timed out.")
        sys.exit(1)

    except FileNotFoundError:
        print(f"  ERROR: Compiler '{compiler}' not found. Make sure g++ is installed.")
        sys.exit(1)


# SECTION 4: PARSE COMPILER ERROR OUTPUT

def parse_errors(error_output, filepath):
    """
    Extract structured error info from raw g++ error text.

    GCC format:  filename.cpp:LINE:COL: error: MESSAGE

    Parameters:
        error_output (str) - raw stderr from compiler
        filepath     (str) - source file path

    Returns:
        list of dicts, each with keys:
            line_number, column_number, error_type, error_message
    """

    pattern = r'([^:]+):(\d+):(\d+):\s*(error|warning):\s*(.+)'
    matches = re.finditer(pattern, error_output, re.MULTILINE)

    errors = []
    for match in matches:
        file, line, col, err_type, message = match.groups()
        errors.append({
            'line_number'   : int(line),
            'column_number' : int(col),
            'error_type'    : err_type,
            'error_message' : message.strip()
        })

    return errors


# SECTION 5: READ A SPECIFIC LINE FROM SOURCE FILE

def read_code_line(filepath, line_number):
    """
    Read a specific line from the source file.

    Parameters:
        filepath    (str) - path to source file
        line_number (int) - 1-based line number

    Returns:
        the code line as string, or empty string if not found
    """

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if 1 <= line_number <= len(lines):
            return lines[line_number - 1].strip()
        return ""

    except Exception:
        return ""


# SECTION 6: EXTRACT FEATURES FROM ONE ERROR

def extract_features(error, filepath):
    """
    Extract the same 28 features used during training.
    Feature groups:
        - Error message keyword features  (14)
        - Code line context features      (10)
        - Structural balance features      (4)
    Plus line_number and column_number = 30 total
    (matches feature_columns.json exactly)

    Parameters:
        error    (dict) - parsed error dict from parse_errors()
        filepath (str)  - source file path (to read code line)

    Returns:
        dict of all features
    """

    msg       = error['error_message'].lower()
    full_msg  = error['error_message']
    code_line = read_code_line(filepath, error['line_number'])

    # ── Error Message Features ────────────────────────────
    msg_features ={
        'msg_has_expected'      : 1 if 'expected'                              in msg else 0,
        'msg_has_declared'      : 1 if ('declared' in msg or 'undeclared' in msg) else 0,
        'msg_has_before'        : 1 if 'before'                                in msg else 0,
        'msg_has_type'          : 1 if 'type'                                  in msg else 0,
        'msg_has_conversion'    : 1 if ('conversion' in msg or 'convert' in msg)  else 0,
        'msg_has_return'        : 1 if 'return'                                in msg else 0,
        'msg_has_control'       : 1 if 'control'                               in msg else 0,
        'msg_has_implicit'      : 1 if 'implicit'                              in msg else 0,
        'msg_has_unknown'       : 1 if 'unknown'                               in msg else 0,
        'msg_mentions_semicolon': 1 if ("';'" in full_msg or 'semicolon' in msg)  else 0,
        'msg_mentions_brace'    : 1 if ("'{'" in full_msg or "'}'" in full_msg or 'brace' in msg) else 0,
        'msg_mentions_paren'    : 1 if ("'('" in full_msg or "')'" in full_msg or 'parenthes' in msg) else 0,
        'msg_length'            : len(full_msg),
        'msg_word_count'        : len(full_msg.split()),
    }

    # ── Code Line Features ────────────────────────────────
    type_keywords = r'\b(int|float|double|char|bool|void|long|short|string|unsigned|const)\b'

    open_braces  = code_line.count('{')
    close_braces = code_line.count('}')
    open_parens  = code_line.count('(')
    close_parens = code_line.count(')')

    code_features = {
        'code_length'          : len(code_line),
        'code_ends_semicolon'  : 1 if code_line.endswith(';') else 0,
        'code_has_declaration' : 1 if re.search(type_keywords, code_line) else 0,
        'code_open_braces'     : open_braces,
        'code_close_braces'    : close_braces,
        'code_open_parens'     : open_parens,
        'code_close_parens'    : close_parens,
        'code_has_assignment'  : 1 if ('=' in code_line and '==' not in code_line) else 0,
        'code_has_comparison'  : 1 if any(op in code_line for op in ['==','!=','<=','>=','<','>']) else 0,
        'code_has_string'      : 1 if ('"' in code_line or "'" in code_line) else 0,
    }

    # ── Structural Balance Features ───────────────────────
    balance_features = {
        'brace_balance' : open_braces  - close_braces,
        'paren_balance' : open_parens  - close_parens,
        'total_braces'  : open_braces  + close_braces,
        'total_parens'  : open_parens  + close_parens,
    }

    # Combine everything + positional info
    all_features = {
        'line_number'   : error['line_number'],
        'column_number' : error['column_number'],
        **msg_features,
        **code_features,
        **balance_features,
    }

    return all_features


# SECTION 7: BUILD FEATURE VECTOR IN CORRECT ORDER

def build_feature_vector(features_dict, feature_cols):
    """
    Arrange features in the exact order the model was trained on.
    This is critical — wrong order = wrong predictions.

    Parameters:
        features_dict (dict) - all extracted features
        feature_cols  (list) - correct feature order from feature_columns.json

    Returns:
        list of feature values in correct order
    """
    return [features_dict.get(col, 0) for col in feature_cols]


# SECTION 8: CLASSIFY ONE ERROR

def classify_error(feature_vector, model, label_map, feature_cols):
    """
    Run the ML model on a single feature vector.

    Parameters:
        feature_vector (list) - ordered feature values
        model          - loaded RandomForestClassifier
        label_map      (dict) - int → category name

    Returns:
        predicted_label (str)  - error category name
        confidence      (float)- prediction confidence 0-100%
    """

    import pandas as pd
    X = pd.DataFrame([feature_vector], columns=feature_cols)

    predicted_int   = model.predict(X)[0]
    probabilities   = model.predict_proba(X)[0]
    confidence      = max(probabilities) * 100

    predicted_label = label_map[str(predicted_int)]

    return predicted_label, confidence


# SECTION 9: PRINT FORMATTED OUTPUT

def print_results(filepath, errors, classifications):
    """
    Print the final diagnosis results in a clean format.

    Parameters:
        filepath        (str)  - source file that was analyzed
        errors          (list) - list of parsed error dicts
        classifications (list) - list of (category, confidence) tuples
    """

    print("\n" + "═" * 62)
    print("   AI COMPILER ERROR DIAGNOSIS SYSTEM — WEEK 9")
    print("═" * 62)
    print(f"  File : {filepath}")
    print(f"  Total Errors Found : {len(errors)}")
    print("═" * 62)

    for i, (error, (category, confidence)) in enumerate(zip(errors, classifications), 1):
        print(f"\n  Error {i}")
        print(f"  {'─' * 55}")
        print(f"  Location   : Line {error['line_number']}, Column {error['column_number']}")
        print(f"  Compiler   : {error['error_message']}")
        print(f"  Category   : {category}")
        print(f"  Confidence : {confidence:.1f}%")

        # Visual confidence bar
        filled = int(confidence / 5)   # 20 blocks = 100%
        bar    = '█' * filled + '░' * (20 - filled)
        print(f"  [{bar}] {confidence:.1f}%")

    print("\n" + "═" * 62)
    print(f"  Classification complete. {len(errors)} error(s) diagnosed.")
    print("═" * 62 + "\n")


# SECTION 10: MAIN ENTRY POINT

def main():
    """
    Main function — orchestrates the full pipeline:
    1. Validate input
    2. Load model
    3. Compile file
    4. Parse errors
    5. Extract features
    6. Classify
    7. Display results
    """

    # ── Step 1: Validate command-line input ───────────────
    if len(sys.argv) < 2:
        print("\n  USAGE: python classify_errors.py <source_file.cpp>")
        print("  EXAMPLE: python classify_errors.py missing_semicolon_1.cpp\n")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"\n  ERROR: File not found → {filepath}\n")
        sys.exit(1)

    print(f"\n  Loading model...")

    # ── Step 2: Load model and metadata ───────────────────
    model, feature_cols, label_map = load_model_and_metadata()
    print(f"  Model loaded : RandomForestClassifier")
    print(f"  Features     : {len(feature_cols)}")
    print(f"  Categories   : {len(label_map)}")

    # ── Step 3: Compile and capture errors ────────────────
    print(f"\n  Compiling: {filepath} ...")
    error_output = compile_and_capture(filepath)

    if error_output is None:
        print(f"\n  ✔ No errors! '{filepath}' compiled successfully.\n")
        sys.exit(0)

    # ── Step 4: Parse errors ──────────────────────────────
    errors = parse_errors(error_output, filepath)

    if not errors:
        print("\n  Could not parse compiler output. Raw output:")
        print(error_output)
        sys.exit(1)

    # ── Step 5 & 6: Extract features + Classify ──────────
    classifications = []

    for error in errors:
        features_dict  = extract_features(error, filepath)
        feature_vector = build_feature_vector(features_dict, feature_cols)
        category, confidence = classify_error(feature_vector, model, label_map,feature_cols)
        classifications.append((category, confidence))

    # ── Step 7: Display results ───────────────────────────
    print_results(filepath, errors, classifications)


# ── Run ───
if __name__ == "__main__":
    main()
